#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

import boto3


def parse_args():
    p = argparse.ArgumentParser(
        description="Invoke a published Amazon Bedrock Flow and create BYOI evaluation JSONL."
    )
    p.add_argument("--tests-json", required=True, help="Path to the test suite JSON.")
    p.add_argument("--flow-id", required=True, help="Bedrock Flow identifier.")
    p.add_argument("--flow-alias-id", required=True, help="Bedrock Flow alias identifier.")
    p.add_argument(
        "--model-identifier",
        default="OnlineShopCustomerSupportFlow",
        help="Value written to modelResponses[0].modelIdentifier.",
    )
    p.add_argument(
        "--out-jsonl",
        default="output_eval_dataset.jsonl",
        help="Destination JSONL path.",
    )
    p.add_argument("--region", default=None, help="AWS Region; otherwise boto3 default.")
    p.add_argument(
        "--enable-trace",
        action="store_true",
        help="Request Flow trace events. Trace is printed, not written to JSONL.",
    )
    return p.parse_args()


def invoke_flow(client, flow_id, alias_id, input_node_name, prompt, enable_trace=False):
    kwargs = {
        "flowIdentifier": flow_id,
        "flowAliasIdentifier": alias_id,
        "inputs": [
            {
                "nodeName": input_node_name,
                "nodeOutputName": "document",
                "content": {"document": prompt},
            }
        ],
    }
    if enable_trace:
        kwargs["enableTrace"] = True

    response = client.invoke_flow(**kwargs)

    response_text = None
    for event in response["responseStream"]:
        print("EVENT:", event)

        if "flowOutputEvent" in event:
            output_event = event["flowOutputEvent"]
            content = output_event.get("content", {})
            if isinstance(content, dict) and "document" in content:
                response_text = content["document"]

    if response_text is None:
        raise RuntimeError("Flow completed without a flowOutputEvent document.")

    return response_text


def main():
    args = parse_args()

    suite = json.loads(Path(args.tests_json).read_text(encoding="utf-8"))
    input_node_name = suite["flowInputNode"]["nodeName"]
    tests = suite["tests"]

    print("Input node name:", input_node_name)

    session = boto3.Session(region_name=args.region)
    client = session.client("bedrock-agent-runtime")

    out_path = Path(args.out_jsonl)
    n_ok = 0

    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        for test in tests:
            test_id = test["id"]
            prompt = test["prompt"]
            reference = test["expected"]

            try:
                response_text = invoke_flow(
                    client,
                    args.flow_id,
                    args.flow_alias_id,
                    input_node_name,
                    prompt,
                    args.enable_trace,
                )
                n_ok += 1
            except Exception as exc:
                print(exc)
                response_text = f"[FLOW_ERROR] {type(exc).__name__}: {exc}"

            record = {
                "prompt": prompt,
                "referenceResponse": reference,
                "modelResponses": [
                    {
                        "response": response_text,
                        "modelIdentifier": args.model_identifier,
                    }
                ],
            }

            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(f"{test_id}: wrote eval line", file=sys.stderr)

    print(
        f"\nWrote {len(tests)} JSONL lines to {out_path} "
        f"({n_ok} flow calls succeeded).",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()

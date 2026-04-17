import argparse
from llm_sdk import Small_LLM_Model
from .io_utils import load_json, save_json
from .pipeline import generate_constrained_json

def main():
    # 1. Setup Command Line Arguments
    parser = argparse.ArgumentParser(description="Function Calling LLM Pipeline")
    parser.add_argument("--functions_definition", default="data/input/functions_definition.json")
    parser.add_argument("--input", default="data/input/function_calling_tests.json")
    parser.add_argument("--output", default="data/output/function_calls.json")
    args = parser.parse_args()

    # 2. Load the data
    functions_def = load_json(args.functions_definition)
    prompts_data = load_json(args.input)

    # # 3. Initialize the Model
    # model = Small_LLM_Model()

    # # 4. Run the pipeline for each prompt
    # results = []
    # for item in prompts_data:
    #     # Wrap the prompt in the format the AI expects
    #     full_prompt = f"System: You are a helpful assistant.\nUser: {item['prompt']}\nAssistant: "

    #     # Generate the JSON
    #     generated_json_str = generate_constrained_json(model, full_prompt, functions_def)

    #     # Strip the original prompt out to isolate the JSON
    #     json_only = generated_json_str.replace(full_prompt, "")

    #     results.append({
    #         "prompt": item["prompt"],
    #         "result": json_only
    #     })

    # # 5. Save the final output
    # save_json(results, args.output)
    # print(f"\nSuccess! Results saved to {args.output}")

if __name__ == "__main__":
    main()

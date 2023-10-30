import openai


if __name__ == '__main__':
        # Set up authentication

    openai.api_key = "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"

    # List models
    models = openai.Model.list()
    for model in models["data"]:
        print(model)
        #if model["org_id"] == "EoRT9gig7M2WZfPU6Q2Ia11X":
         #   print(model["id"], model["display_name"])


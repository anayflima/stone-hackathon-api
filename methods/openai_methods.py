
def get_response_from_model(client, question, historical_messages):
    
    historical_messages.append({"role": "user", "content": question})
    messages_list = [
                {"role": m["role"], "content": m["content"]}
                for m in historical_messages
                ]
    print(messages_list)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_list
        )
    response_text = response.choices[0].message.content
    historical_messages.append({"role": "assistant", "content": response_text})
    return response_text
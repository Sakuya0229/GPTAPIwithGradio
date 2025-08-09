from openai import OpenAI

client = OpenAI()  # 請填入你自己的金鑰

try:
    response = client.responses.create(
        model="gpt-4o",
        input="今天天氣怎麼樣？",
        instructions="你是一個幽默又簡短的助手",
    )
    print("✅ 呼叫成功！")
    print(response.output_text)
except Exception as e:
    print("❌ 呼叫失敗！")
    print(type(e), e)

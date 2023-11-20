import time
from pathlib import Path
from openai import OpenAI
from decouple import config
from openai.types.beta import Thread

client = OpenAI(
    api_key=config("OPENAI_API_KEY")
)


def list_messages(thread) -> None:
    thread_messages = client.beta.threads.messages.list(thread.id,)
    print(thread_messages.data)


def main():
    # step 1 - set assistant
    assistant = client.beta.assistants.create(
        name="Math Tutor",
        instructions="Ты - профессиональный инженер по акустическому оборудованию и системам управления, "
                     "можешь написать и выполнить код для решения задачи",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview"
    )

    # step 2 make new thread
    thread: Thread = client.beta.threads.create()

    # step 3 add a message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Мне нужно подобрать акустику в помещение 8 x 4 метра для проведения конференций и просмотра контента"
                "Поможешь мне собрать спецификацию на оборудовании бренда LD Systems / Adam Hall?"
    )

    # step 4 run assistance
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Пожалуйста пиши максимально конкретно и технически грамотно. "
                     "Клиент хорошо разбирается в вопросе."
    )

    # step 5 check the run status
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )

    while True:
        while run.status == "in_progress":
            time.sleep(1)
            print(type(run.status))
            print(run.status)
            continue

        else:
            print(run.status)

    # step 6 get response
    # messages = client.beta.threads.messages.list(
    #     thread_id=thread.id
    # )
    #
    # print(messages)

    # for i in messages:
    #     print(f"{i.role} at {i.created_at}:\n{i.content}\n")


if __name__ == '__main__':
    main()

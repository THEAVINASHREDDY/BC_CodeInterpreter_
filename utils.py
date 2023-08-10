from codeinterpreterapi import CodeInterpreterSession
import streamlit as st


async def get_images(prompt: str, files: list = None):
    if files is None:
        files = []
    with st.chat_message("user"):
        st.write(prompt)
    with st.spinner():
        async with CodeInterpreterSession(model='gpt-4-32k') as session:
            response = await session.generate_response(
                prompt,
                files=files
            )
            with st.chat_message("assistant"):
                st.write(response.content)

                for file in response.files:
                    st.image(file.get_image(), caption=prompt, use_column_width=True)
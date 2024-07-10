import streamlit as st
# for i in range(1,10):
print("AA")
with st.chat_message("user"):
    st.write("hello")
with st.chat_message("ai"):
    st.write("what can i help you")
prompt = st.chat_input("say something")
if prompt :
    print("prompt = ", end="")
    print(prompt)
    with st.chat_message("user"):
        st.write(prompt)

# dialog = st.beta_container()
# show_dialog_button = st.button('Show Dialog')
# if show_dialog_button:
#     with dialog:
#         st.write("This is the content of the dialog")
#         # 在这里添加你的对话框内容
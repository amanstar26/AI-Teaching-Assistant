import streamlit as st
import base64

from embedding_model import load_embedding_model
from pdf_processor import extract_text_from_pdf, chunk_text
from vector_store import (
    create_faiss_index,
    search_chunks,
    save_index,
    load_index,
    save_chunks,
    load_chunks,
    vector_store_exists,
    save_metadata,
    is_same_pdf
)
from rag_engine import (
    generate_answer,
    generate_question_paper,
    generate_flashcards,
    parse_flashcards,
    generate_study_plan,
    generate_ppt_content
)
from qp import (
    create_question_paper_pdf
)
from study_plan import (
    create_study_plan_pdf
)
from ppt_gen import create_ppt
from streamlit_pdf_viewer import pdf_viewer


st.set_page_config(
    page_title="AI Teaching Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Teaching Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processing" not in st.session_state:
    st.session_state.processing = False

if "current_request" not in st.session_state:
    st.session_state.current_request = None

if "request_queue" not in st.session_state:
    st.session_state.request_queue = []

if "answer_mode" not in st.session_state:
    st.session_state.answer_mode = "hybrid"

if "chat_cache" not in st.session_state:
    st.session_state.chat_cache = {}


with st.sidebar:

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None

if uploaded_file:

    if (
        st.session_state.current_pdf
        != uploaded_file.name
    ):

        st.session_state.chat_cache = {}

        st.session_state.current_pdf = (
            uploaded_file.name
        )

    pdf_path = f"uploads/{uploaded_file.name}"

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if (vector_store_exists() and is_same_pdf(uploaded_file.name)):

        chunks = load_chunks()
        index = load_index()
        model = load_embedding_model()

        st.success(
            f"📄 Current Document: {uploaded_file.name}"
        )

    else:

        with st.spinner("Processing PDF..."):

            text = extract_text_from_pdf(pdf_path)

            chunks = chunk_text(text)

            index, model = create_faiss_index(chunks)

            save_index(index)
            save_chunks(chunks)
            save_metadata(
                uploaded_file.name
            )
        st.success(
            f"📄 Current Document: {uploaded_file.name}"
        )

    left_col, right_col = st.columns([1.2, 1])

    with left_col:

        st.subheader("📄 PDF Viewer")

        pdf_viewer(
            pdf_path,
            width="100%",
            height=820
        )

    with right_col:
        
        st.subheader("💬 Chat with AI")
        tool1, tool2, tool3, tool4 = st.columns(4)

        with tool1:
            qp_btn = st.button(
                "📝 Question Paper",
                use_container_width=True
            )

        with tool2:
            flash_btn = st.button(
                "🃏 Flashcards",
                use_container_width=True
            )

        with tool3:
            ppt_btn = st.button(
                "📊 PPT",
                use_container_width=True
            )

        with tool4:
            study_btn = st.button(
                "📅 Study Plan",
                use_container_width=True
            )

        if qp_btn:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Generate Question Paper"
                }
            )

            st.session_state.request_queue.append(
                {
                    "type": "question_paper"
                }
            )

            st.rerun()

        if flash_btn:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Generate Flashcards"
                }
            )

            st.session_state.request_queue.append(
                {
                    "type": "flashcards"
                }
            )


            st.rerun()

        if ppt_btn:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Generate PPT"
                }
            )

            st.session_state.request_queue.append(
                {
                    "type": "ppt"
                }
            )

            st.rerun()

        if study_btn:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Generate Study Plan"
                }
            )

            st.session_state.request_queue.append(
                {
                    "type": "study_plan"
                }
            )

            st.rerun()
        
        st.markdown("""
        <style>

        .chat-container {
            height: 700px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 10px;
        }

        </style>
        """, unsafe_allow_html=True)
        
        chat_area = st.container(height=650)
        
        if (
            not st.session_state.processing
            and
            len(st.session_state.request_queue) > 0
        ):

            st.session_state.current_request = (
                st.session_state.request_queue.pop(0)
            )

            st.session_state.processing = True

            st.rerun()
        
        with chat_area:

            for msg in st.session_state.messages:

                with st.chat_message(msg["role"]):

                    if msg.get("type") in [
                        "file",
                        "study_plan_file",
                        "ppt"
                    ]:

                        st.success(msg["content"])
                        if msg.get("type") == "file":

                            filename = "question_paper.pdf"
                            mime = "application/pdf"
                            btn_text = "📥 Download Question Paper"

                        elif msg.get("type") == "study_plan_file":

                            filename = "study_plan.pdf"
                            mime = "application/pdf"
                            btn_text = "📥 Download Study Plan"

                        elif msg.get("type") == "ppt":

                            filename = "chapter_presentation.pptx"
                            mime = (
                                "application/vnd.openxmlformats-officedocument."
                                "presentationml.presentation"
                            )
                            btn_text = "📥 Download PPT"

                        with open(
                            msg["file_path"],
                            "rb"
                        ) as f:

                            st.download_button(
                                btn_text,
                                data=f,
                                file_name=filename,
                                mime=mime,
                                key=msg["file_path"]
                            )
                    elif msg.get("type") == "flashcards":

                        st.success(
                            f"Generated {len(msg['cards'])} Flashcards"
                        )

                        for i, card in enumerate(msg["cards"]):

                            with st.container(border=True):

                                st.markdown(
                                    f"### 🃏 Flashcard {i+1}"
                                )

                                st.markdown(
                                    f"**Question**\n\n{card['question']}"
                                )

                                with st.expander("Show Answer"):
                                    st.success(card["answer"])
                    else:

                        st.write(
                            msg["content"]
                        )

            for req in st.session_state.request_queue:

                if req["type"] == "chat":

                    with st.chat_message("user"):
                        st.write(req["question"])

                    with st.chat_message("assistant"):
                        st.info("⏳ Queued")
            if (
                st.session_state.processing
                and
                st.session_state.current_request
            ):
                request = st.session_state.current_request
                request_type = request["type"]
                
                with st.chat_message("assistant"):

                    if request_type == "question_paper":
                        st.write(
                            "📄 Generating Question Paper..."
                        )
                    elif request_type == "flashcards":
                        st.write(
                            "🃏 Generating Flashcards..."
                        )
                    elif request_type == "study_plan":
                        st.write(
                            "Generating Study Plan..."
                        )
                    elif request_type == "ppt":
                        st.write(
                            "Generating PPT..."
                        )
                    else:
                        st.write("Thinking...")

        st.caption(
            f"Current Answer Mode: {st.session_state.answer_mode.title()}"
        )
        question = st.chat_input(
            "Ask a question about the PDF..."
        )

        if (
            st.session_state.processing
            and
            st.session_state.current_request
        ):
            request = st.session_state.current_request
            request_type = request["type"]
            
            # QUESTION PAPER
            if request_type == "question_paper":
                
                print("\nGenerating question paper...")
                context_for_generation = "\n\n".join(chunks[:25])
                
                paper = generate_question_paper(context_for_generation)
                
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": paper
                    }
                )
                print("Creating Question Paper PDF...")
                pdf_file = create_question_paper_pdf(
                    paper
                )
                print("Question Paper PDF created")
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "type": "file",
                        "content":
                        "📄 Question Paper Generated Successfully",
                        "file_path": pdf_file
                    }
                )

                st.session_state.processing = False
                st.session_state.current_request = None

                st.rerun()
            
            elif request_type == "flashcards":
                
                context_for_generation = "\n\n".join(chunks[:25])
                
                flashcards_text = generate_flashcards(context_for_generation)

                print("\n===== FLASHCARDS RAW OUTPUT =====")
                print(flashcards_text)
                print("================================")
                cards = parse_flashcards(
                    flashcards_text
                )

                if not cards:

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content":
                            f"Flashcard parsing failed.\n\nRaw Output:\n\n{flashcards_text}"
                        }
                    )

                else:

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "type": "flashcards",
                            "cards": cards
                        }
                    )

                st.session_state.processing = False
                st.session_state.current_request = None

                st.rerun()
            
            elif request_type == "study_plan":

                context_for_generation = (
                    "\n\n".join(chunks[:25])
                )

                plan = generate_study_plan(
                    context_for_generation
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": plan
                    }
                )

                pdf_file = create_study_plan_pdf(
                    plan
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "type": "study_plan_file",
                        "content":
                        "📚 Study Plan Generated Successfully",
                        "file_path": pdf_file
                    }
                )

                st.session_state.processing = False
                st.session_state.current_request = None

                st.rerun()
            
            elif request_type == "ppt":

                context_for_generation = (
                    "\n\n".join(chunks[:25])
                )

                ppt_content = generate_ppt_content(
                    context_for_generation
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": ppt_content
                    }
                )

                ppt_file = create_ppt(
                    ppt_content
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "type": "ppt",
                        "content":
                        "📚 PPT Generated Successfully",
                        "file_path": ppt_file
                    }
                )

                st.session_state.processing = False
                st.session_state.current_request = None

                st.rerun()

            # NORMAL CHAT
            elif request_type == "chat":

                question = request["question"]

                mode = request.get(
                    "mode",
                    "hybrid"
                )

                cache_key = (
                    mode
                    + "|"
                    + question.lower().strip()
                )

                if (
                    cache_key
                    in st.session_state.chat_cache
                ):

                    print(
                        "⚡ Answer served from cache"
                    )

                    answer = st.session_state.chat_cache[
                            cache_key
                        ]
                    
                    st.toast("⚡ Answer served from cache")
                    
                else:

                    results = search_chunks(
                        question,
                        index,
                        model,
                        chunks,
                        top_k=8
                    )

                    context = "\n\n".join(results)

                    answer = generate_answer(
                        question,
                        context,
                        mode
                    )
                    st.session_state.chat_cache[
                        cache_key
                    ] = answer

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                st.session_state.processing = False
                st.session_state.current_request = None

                st.rerun()

        if question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            if question.strip().lower() == "/opt":

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "type": "options",
                        "content": """
            Which type of answer would you like?

            1️⃣ Document

            2️⃣ AI

            3️⃣ Hybrid (Document + Additional AI Explanation)

            Current Mode: {}
                        """.format(
                            st.session_state.answer_mode.title()
                        )
                    }
                )

                st.rerun()
            
            elif question.strip() == "1":

                st.session_state.answer_mode = "document"

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content":
                        "✅ Answer mode changed to Document Only"
                    }
                )

                st.rerun()

            elif question.strip() == "2":

                st.session_state.answer_mode = "ai"

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content":
                        "✅ Answer mode changed to AI Only"
                    }
                )

                st.rerun()

            elif question.strip() == "3":

                st.session_state.answer_mode = "hybrid"

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content":
                        "✅ Answer mode changed to Hybrid"
                    }
                )

                st.rerun()

            st.session_state.request_queue.append(
                {
                    "type": "chat",
                    "question": question,
                    "mode": st.session_state.answer_mode
                }
            )

            st.rerun()
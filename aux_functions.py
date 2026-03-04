

def footer():
    import streamlit.components.v1 as components
    import streamlit as st
    st.markdown("---")

    components.html(
        """
        <script type="text/javascript"
            src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js"
            data-name="bmc-button"
            data-slug="pedromoraia"
            data-color="#FFDD00"
            data-emoji=""
            data-font="Cookie"
            data-text="Ajuda-nos a ajudar"
            data-outline-color="#000000"
            data-font-color="#000000"
            data-coffee-color="#ffffff">
        </script>
        """,
        height=80
    )
    st.caption("Feito com ❤️ por [Pedro Maltez](https://pedromaltex.github.io/Portfolio).")
    st.caption(
        "Esta simulação é educativa. Não substitui planeamento financeiro personalizado."
    )
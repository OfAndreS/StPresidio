"""Apresentação sobre o Microsoft Presidio construída com pystslides."""

from pathlib import Path

import streamlit as st

from pystslides import (
    HighlightLevel,
    HighlightSpan,
    Presentation,
    PresentationTheme,
    get_editorial_assets_dir,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _highlight_terms(
    text: str,
    terms: tuple[tuple[str, str], ...],
    style: HighlightLevel | tuple[float, ...],
    *,
    high_threshold: float = 0.75,
) -> list[HighlightSpan]:
    """Localiza trechos em ordem no texto e constrói os `HighlightSpan` correspondentes."""
    spans: list[HighlightSpan] = []
    cursor = 0
    for idx, (term, label) in enumerate(terms):
        start = text.index(term, cursor)
        end = start + len(term)
        cursor = end
        if isinstance(style, HighlightLevel):
            spans.append(HighlightSpan(start, end, label, level=style))
        else:
            spans.append(
                HighlightSpan.from_score(
                    start,
                    end,
                    label,
                    style[idx],
                    high_threshold=high_threshold,
                )
            )
    return spans

# Configuração do tema visual da apresentação
custom_theme = PresentationTheme(
    divider_color="#000000",
)

# Inicialização da apresentação e definição das seções de slides
with Presentation(
    title="Microsoft Presidio",
    assets_dir=get_editorial_assets_dir(),
    auto_number=False,
    brand_label="Microsoft Presidio",
    show_toc=True,
    theme=custom_theme,
) as deck:
    # Capa da apresentação
    deck.divider()

    deck.split_slide(
        "Microsoft Presidio",
        "Mapeamento e classificação de dados sensíveis",
        media="classification_network.png",
        media_position="right",
        media_vertical_align="center",
        kicker="Microsoft Presidio",
    )

    deck.divider()

    # =========================================================================
    # Seção 1: Segurança — Introdução e categorias de rotulagem de dados (PII)
    # =========================================================================
    deck.kicker("Security")

    # 1.0 Introdução
    deck.topic("01 ) Introdução")
    deck.paragraph(
        "O Microsoft Presidio é um kit de ferramentas open-source "
        "(em Python e APIs REST) criado para detectar e anonimizar dados "
        "pessoais sensíveis (PII) em textos, imagens e dados estruturados. "
        "Ele ajuda organizações a proteger a privacidade e atender a normas "
        "como a LGPD no Brasil."
    )

    # 1.1 Ferramenta de rotulagem
    deck.topic("1.1 ) Ferramenta de rotulagem")

    # 1.2.1 Identidade e Contato
    deck.split_slide(
        "Identidade e Contato",
        (
            "Dados pessoais que identificam e permitem localizar ou entrar "
            "em contato direto com um indivíduo."
        ),
        media="ai_shield_animated.svg",
        media_position="left",
        media_vertical_align="center",
    )
    deck.styled_table(
        {
            "Categoria": [
                "PERSON",
                "EMAIL_ADDRESS",
                "PHONE_NUMBER",
                "LOCATION",
                "NRP",
                "DATE_TIME",
            ],
            "Descrição": [
                "Nome completo de uma pessoa.",
                "Endereço de correio eletrônico.",
                "Número de telefone com suporte ajustável para vários países.",
                "Nomes de locais políticos ou geográficos como cidades e países.",
                "Nacionalidade ou afiliação religiosa e política de uma pessoa.",
                "Datas e tempos absolutos ou relativos (como data de nascimento).",
            ],
        }
    )

    # 1.2.2 Dados Financeiros
    deck.split_slide(
        "Dados Financeiros",
        (
            "Informações relacionadas a contas, transações, pagamentos, "
            "rendimentos e à situação econômica ou fiscal de uma pessoa."
        ),
        media="classification_nodes_animated.svg",
        media_position="right",
        media_vertical_align="center",
    )
    deck.styled_table(
        {
            "Categoria": ["CREDIT_CARD", "CRYPTO", "IBAN_CODE"],
            "Descrição": [
                "Número de cartão de crédito de 12 a 19 dígitos.",
                "Endereço de carteira de criptomoeda (como Bitcoin).",
                "Número internacional de conta bancária para transações globais.",
            ],
        }
    )

    # 1.2.3 Redes e Dispositivos
    deck.split_slide(
        "Redes e Dispositivos",
        (
            "Registros técnicos gerados por conexões digitais e equipamentos "
            "eletrônicos utilizados durante o acesso a sistemas."
        ),
        media="coverage_laptop.png",
        media_position="left",
        media_vertical_align="center",
    )
    deck.styled_table(
        {
            "Categoria": ["IP_ADDRESS", "MAC_ADDRESS", "URL"],
            "Descrição": [
                "Endereço de protocolo de internet em formato IPv4 ou IPv6.",
                "Identificador único para interfaces de rede física.",
                "Endereço ou identificador único de recursos na internet.",
            ],
        }
    )

    # 1.2.4 Documentos Globais
    deck.split_slide(
        "Documentos Globais",
        (
            "Registros oficiais de identificação emitidos por autoridades "
            "para reconhecimento legal e trânsito em âmbito internacional."
        ),
        media="ai_shield_animated.svg",
        media_position="right",
        media_vertical_align="center",
    )
    deck.styled_table(
        {
            "Categoria": ["PASSPORT"],  # Sugestão adicionada para preencher o tópico
            "Descrição": [
                "Número de passaporte emitido para identificação e viagens internacionais.",
            ],
        }
    )

    # 1.2.5 Documentos Regionais
    deck.split_slide(
        "Documentos Regionais",
        (
            "Registros oficiais emitidos por órgãos governamentais locais "
            "para identificação civil e fiscal em território nacional."
        ),
        media="access_governance_animated.svg",
        media_position="left",
        media_vertical_align="center",
    )
    deck.styled_table(
        {
            "Categoria": ["MEDICAL_LICENSE"],
            "Descrição": [
                "Números regionais de licenças e registros profissionais médicos.",
            ],
        }
    )

    deck.divider()

    # =========================================================================
    # Seção 2: Anonimização — Conceitos e técnicas de proteção de dados (PII)
    # =========================================================================
    deck.kicker("Data Discovery")

    # 2.0 Data Anonymization
    deck.topic("02 ) Data Anonymization")
    deck.paragraph(
        "Após identificar os dados sensíveis, a anonimização transforma os "
        "trechos confidenciais para proteger a identidade dos titulares sem "
        "inviabilizar o uso operacional ou analítico do texto. Considere a "
        "frase original abaixo como exemplo de partida:"
    )
    frase_original = (
        "A paciente Maria da Silva pagou a consulta com o cartão final 1234."
    )
    deck.highlighted_text(
        frase_original,
        spans=_highlight_terms(
            frase_original,
            (("Maria da Silva", "PESSOA"), ("1234", "CARTÃO")),
            HighlightLevel.HIGH,
        ),
    )

    # 2.1 Técnicas de Anonimização
    deck.topic("2.1 ) Técnicas de Anonimização")

    # 2.1.1 Censura Direta
    deck.split_slide(
        "Censura Direta",
        (
            "A ferramenta substitui a palavra sensível pelo nome da categoria "
            "correspondente. O nome do cliente desaparece e o espaço recebe apenas "
            "a etiqueta da entidade, bloqueando totalmente a leitura do dado."
        ),
        media="remediation_automation_animated.svg",
        media_position="left",
        media_vertical_align="center",
    )
    texto_censura = (
        "Texto tratado: A paciente [PESSOA] pagou a consulta com o cartão final [NUMERO]."
    )
    deck.highlighted_text(
        texto_censura,
        spans=_highlight_terms(
            texto_censura,
            (("[PESSOA]", "CENSURA"), ("[NUMERO]", "CENSURA")),
            HighlightLevel.LOW,
        ),
    )

    # 2.1.2 Mascaramento Parcial
    deck.split_slide(
        "Mascaramento Parcial",
        (
            "O sistema oculta apenas parte da informação com caracteres especiais, "
            "preservando as primeiras letras ou dígitos e trocando o restante por "
            "asteriscos para permitir conferência sem expor o dado completo."
        ),
        media="discovery_analytics_animated.svg",
        media_position="right",
        media_vertical_align="center",
    )
    texto_mascara = (
        "Texto tratado: A paciente M**** da S**** pagou a consulta com o cartão final 1***."
    )
    deck.highlighted_text(
        texto_mascara,
        spans=_highlight_terms(
            texto_mascara,
            (("M**** da S****", "MÁSCARA"), ("1***", "MÁSCARA")),
            HighlightLevel.LOW,
        ),
    )

    # 2.1.3 Criptografia Irreversível
    deck.split_slide(
        "Criptografia Irreversível",
        (
            "O programa aplica uma função matemática de hash para transformar dados "
            "legíveis em códigos irreversíveis. Como entradas iguais geram o mesmo "
            "código, é possível cruzar tabelas sem revelar a identidade real."
        ),
        media="database_cluster_animated.svg",
        media_position="left",
        media_vertical_align="center",
    )
    texto_hash = (
        "Texto tratado: A paciente 8f2a1b pagou a consulta com o cartão final a7b9c1."
    )
    deck.highlighted_text(
        texto_hash,
        spans=_highlight_terms(
            texto_hash,
            (("8f2a1b", "HASH"), ("a7b9c1", "HASH")),
            HighlightLevel.LOW,
        ),
    )

    # 2.1.4 Pseudonimização
    deck.split_slide(
        "Pseudonimização",
        (
            "A informação verdadeira é substituída por um dado fictício gerado "
            "aleatoriamente no mesmo formato. O texto mantém leitura natural para "
            "testes e análises enquanto preserva integralmente a privacidade."
        ),
        media="workflow_sync_animated.svg",
        media_position="right",
        media_vertical_align="center",
    )
    texto_pseudonimo = (
        "Texto tratado: A paciente Carla Mendes pagou a consulta com o cartão final 9876."
    )
    deck.highlighted_text(
        texto_pseudonimo,
        spans=_highlight_terms(
            texto_pseudonimo,
            (("Carla Mendes", "PSEUDÔNIMO"), ("9876", "PSEUDÔNIMO")),
            HighlightLevel.HIGH,
        ),
    )

    deck.divider()

    # =========================================================================
    # Seção 3: Confiabilidade — Arquitetura de funcionamento e código prático
    # =========================================================================
    deck.kicker("Confiability")

    # 3.0 Funcionamento
    deck.topic("03 ) Funcionamento")

    # Diagrama de fluxo entre Analyzer e Anonymizer
    deck.mermaid(
        """
        flowchart LR

            A[<b>Analyzer</b><br/>Detecção & Classificação PII]
            B[<b>Anonymizer</b><br/>Mascaramento & Criptografia]

            T([Texto]) -.-> A
            I([Imagem]) -.-> A
            D([Tabela]) -.-> A

            A --> B

            B --> S[/Dados Protegidos/]
        """,
        border="none",
    )

    # 3.1 Principais Funções
    deck.topic("3.1 ) Principais Funções")

    # 3.1.1 AnalyzerEngine — Detecção automática de entidades PII
    deck.split_slide(
        "AnalyzerEngine",
        (
            "Esse componente funciona como o inspetor do sistema. A função "
            "dele é ler o texto original e procurar informações confidenciais "
            "usando as técnicas que estudamos anteriormente. O resultado gerado "
            "é um mapa indicando a posição exata de cada palavra sensível."
        ),
        media="lock_verification_animated.svg",
        media_position="left",
        media_vertical_align="center",
    )

    deck.code_block(
        code="""
            motor_analise = AnalyzerEngine()

            texto_exemplo = "My name is Jonh Lennon and my number is +1 305 555-1234"

            resultados = motor_analise.analyze(
                text=texto_exemplo,
                language="en",
            )

            print(resultados)
        """,
        output="""[
            \ntype: PERSON, start: 11, end: 22, score: 0.85, 
            \ntype: PHONE_NUMBER, start: 40, end: 55, score: 0.75
            \n]""",
        border="black",
        output_border="grey",
    )

    # 3.1.2 PatternRecognizer — Regras customizadas com expressões regulares
    deck.split_slide(
        "PatternRecognizer",
        (
            "A biblioteca original já reconhece várias entidades globais de "
            "forma automática. O desenvolvedor utiliza essa função específica "
            "para ensinar o sistema a encontrar formatos novos que existem "
            "apenas dentro da rotina da empresa."
        ),
        media="code_review_animated.svg",
        media_position="right",
        media_vertical_align="center",
    )

    deck.code_block(
        code=r"""
            analyzer_engine = AnalyzerEngine()

            ticket_pattern = Pattern(
                name="support_ticket_rule",
                regex="TICKET-[0-9]{4}",
                score=0.9
            )

            custom_recognizer = PatternRecognizer(
                supported_entity="SUPPORT_TICKET",
                patterns=[ticket_pattern],
                supported_language="en"
            )

            analyzer_engine.registry.add_recognizer(custom_recognizer)

            sample_text = "The customer reported an access failure in TICKET-4598 this morning."
            results = analyzer_engine.analyze(text=sample_text, language="en")

            print(results)
        """,
        output="[type: SUPPORT_TICKET, start: 43, end: 54, score: 0.9]",
        border="black",
        output_border="grey",
    )

    # 3.1.3 AnonymizerEngine — Aplicação de máscaras e ocultação de dados
    deck.split_slide(
        "AnonymizerEngine",
        (
            "Esse componente é o responsável pela edição final do arquivo. O "
            "sistema recebe as posições encontradas pelo motor de análise e "
            "aplica as técnicas de ocultação escolhidas pelo programador."
        ),
        media="metrics_dashboard_animated.svg",
        media_position="left",
        media_vertical_align="center",
    )

    deck.code_block(
        code=r"""
            analyzer_engine = AnalyzerEngine()
            anonymizer_engine = AnonymizerEngine()

            sample_text = "My phone number is +1 305 555-1234."
            results = analyzer_engine.analyze(text=sample_text, language="en")

            operators_config = {
                "PHONE_NUMBER": OperatorConfig(
                    "mask", {"chars_to_mask": 4, "masking_char": "*", "from_end": True}
                )
            }

            safe_text = anonymizer_engine.anonymize(
                text=sample_text,
                analyzer_results=results,
                operators=operators_config
            )

            print(safe_text.text)
        """,
        output="My phone number is +1 305 555-****.",
        border="black",
        output_border="grey",
    )

    deck.divider()

    # =========================================================================
    # Seção 4: Aplicação — Exemplos práticos com texto, tabela e imagem
    # =========================================================================
    deck.kicker("Application")

    # 4.0 Exemplos por Tipo de Dado
    deck.topic("04 ) Exemplos por Tipo de Dado")
    deck.paragraph(
        "Para consolidar o funcionamento do Microsoft Presidio na prática, "
        "a seguir estão três cenários aplicados a formatos distintos: "
        "texto livre (e-mail), dados estruturados (tabela CSV) e imagem (raio-X)."
    )

    # 4.1 Texto — E-mail com dados pessoais (CPF + Cartão de crédito)
    deck.topic("4.1 ) Texto — E-mail com Dados Pessoais")
    deck.split_slide(
        "Análise de E-mail (CPF e Cartão)",
        (
            "Em canais de suporte por e-mail, clientes enviam informações "
            "pessoais para agilizar o atendimento. Além das entidades nativas "
            "do idioma, adicionamos regras de regex para capturar formatos "
            "brasileiros de CPF e cartão de crédito."
        ),
        media="code_review_animated.svg",
        media_position="left",
        media_vertical_align="center",
    )

    deck.code_block(
        code=r"""
            from presidio_analyzer import Pattern, PatternRecognizer

            molde_cpf = r"\d{3}\.\d{3}\.\d{3}\s?\d{2}"
            reconhecedor_cpf = PatternRecognizer(
                supported_entity="CPF",
                patterns=[Pattern(name="padrao_cpf", regex=molde_cpf, score=0.9)],
                supported_language="pt",
            )
            analisador.registry.add_recognizer(reconhecedor_cpf)

            molde_cartao = r"\d{4}\s\d{4}\s\d{4}\s\d{4}"
            reconhecedor_cartao = PatternRecognizer(
                supported_entity="CREDIT_CARD",
                patterns=[Pattern(name="padrao_cartao", regex=molde_cartao, score=0.9)],
                supported_language="pt",
            )
            analisador.registry.add_recognizer(reconhecedor_cartao)

            resultados = analisador.analyze(text=texto_email, language="pt")
        """,
        border="black",
    )

    email_exemplo = (
        "Assunto: Ficha de cadastro para exame admissional\n\n"
        "Olá equipe de recursos humanos. Escrevo para enviar as informações da ficha de saúde.\n\n"
        "O meu nome completo é Eduardo Pereira Silva. Eu moro na cidade de Curitiba.\n"
        "Vocês podem falar comigo pelo celular (41) 98765 1234 ou pelo e-mail "
        "carlos.pereira@exemplo.com.br.\n"
        "O documento vinculado ao contrato é o CPF 123.456.789 10. "
        "\nO cartão de crédito é 4095 2609 9393 4932.\n\n"
        "Atenciosamente, Eduardo."
    )
    deck.highlighted_text(
        email_exemplo,
        spans=_highlight_terms(
            email_exemplo,
            (
                ("Eduardo Pereira Silva", "PERSON"),
                ("Curitiba", "LOCATION"),
                ("carlos.pereira@exemplo.com.br", "EMAIL_ADDRESS"),
                ("123.456.789 10", "CPF"),
                ("4095 2609 9393 4932", "CREDIT_CARD"),
                ("Eduardo", "PERSON"),
            ),
            (0.85, 0.85, 1.00, 0.90, 0.90, 0.85),
        ),
    )

    # 4.2 Tabela — Varredura em dados estruturados (CSV)
    deck.topic("4.2 ) Tabela — Varredura em CSV")
    deck.split_slide(
        "Dados Tabulares com BatchAnalyzerEngine",
        (
            "Planilhas e relatórios exportados em CSV costumam reunir colunas "
            "cadastrais e campos de texto livre com comentários. O analisador "
            "em lote percorre cada coluna do dicionário e mapeia onde há "
            "dados pessoais expostos antes do compartilhamento."
        ),
        media="database_cluster_animated.svg",
        media_position="right",
        media_vertical_align="center",
    )

    deck.code_block(
        code=r"""
            import pandas as pd
            from presidio_analyzer import BatchAnalyzerEngine

            df_csv = pd.read_csv("raw_test.csv")
            batch_analyzer = BatchAnalyzerEngine(analyzer_engine=analisador)

            dados_dict = df_csv.to_dict(orient="list")
            resultados_tabela = list(
                batch_analyzer.analyze_dict(dados_dict, language="en")
            )
        """,
        border="black",
    )

    tabela_csv = {
        "id": ["1", "2", "3"],
        "name": ["John", "Jill", "Jack"],
        "city": ["New York", "Los Angeles", "Chicago"],
        "comments": [
            "called him yesterday to confirm he requested to call back in 2 days",
            "accepted the offer license number AC432223",
            "need to call him at phone number 212-555-5555",
        ],
    }
    destaques_tabela = {
        ("name", 0): [HighlightSpan.from_score(0, 4, "PERSON", 0.85)],
        ("name", 1): [HighlightSpan.from_score(0, 4, "PERSON", 0.85)],
        ("name", 2): [HighlightSpan.from_score(0, 4, "PERSON", 0.85)],
        ("city", 0): [HighlightSpan.from_score(0, 8, "LOCATION", 0.85)],
        ("city", 1): [HighlightSpan.from_score(0, 11, "LOCATION", 0.85)],
        ("city", 2): [HighlightSpan.from_score(0, 7, "LOCATION", 0.85)],
        ("comments", 0): _highlight_terms(
            tabela_csv["comments"][0],
            (("yesterday", "DATE_TIME"), ("2 days", "DATE_TIME")),
            (0.85, 0.85),
        ),
        ("comments", 2): _highlight_terms(
            tabela_csv["comments"][2],
            (("212-555-5555", "PHONE_NUMBER"),),
            (0.75,),
        ),
    }
    deck.styled_table(tabela_csv, highlights=destaques_tabela)

    # 4.3 Imagem — Detecção em exame de Raio-X
    deck.topic("4.3 ) Imagem — Exame de Raio-X")
    deck.split_slide(
        "Data Discovery em Imagens Médicas",
        (
            "Parte das informações sensíveis permanece oculta em arquivos "
            "não estruturados, como documentos digitalizados e exames médicos. "
            "Combinando OCR e análise contextual, o módulo de imagem detecta "
            "e oculta identificadores gravados diretamente sobre o exame."
        ),
        media="ai_shield_animated.svg",
        media_position="left",
        media_vertical_align="center",
    )

    deck.code_block(
        code=r"""
            from PIL import Image
            from presidio_image_redactor import ImagePiiVerifyEngine

            imagem = Image.open("pulmao1.png")
            verify_engine = ImagePiiVerifyEngine()

            # Destaca as entidades detectadas com os respectivos rótulos
            imagem_rotulada = verify_engine.verify(
                imagem, display_image=True, show_text_annotation=True
            )

            # Aplica apenas a ocultação visual sobre os trechos sensíveis
            imagem_protegida = verify_engine.verify(
                imagem, display_image=True, show_text_annotation=False
            )
        """,
        border="black",
    )

    deck.image_gallery(
        [
            (DATA_DIR / "pulmao1.png", "Original — Exame com dados expostos"),
            (DATA_DIR / "pulmao2.png", "Verificação — show_text_annotation=True"),
            (DATA_DIR / "pulmao3.png", "Ocultação — show_text_annotation=False"),
        ],
        bordered=True,
    )

    deck.divider()

    # =========================================================================
    # Seção 5: Encerramento — Simulador interativo e quiz de fixação
    # =========================================================================
    deck.kicker("Interactive")

    # 5.0 Prática Interativa
    deck.topic("05 ) Prática Interativa")
    deck.split_slide(
        "Experimente na Prática",
        (
            "Para encerrar, ajuste o limiar de confiança da detecção de "
            "entidades, compare o mesmo registro antes e depois da "
            "anonimização e teste os conceitos aprendidos no quiz final."
        ),
        media="interactive_quiz_animated.svg",
        media_position="right",
        media_vertical_align="center",
    )

    # 5.1 Simulador de Detecção e Anonimização
    deck.topic("5.1 ) Simulador de Detecção e Anonimização")
    limiar_alto = st.slider(
        "Limiar mínimo para confiança ALTA (verde)",
        min_value=0.55,
        max_value=0.98,
        value=0.75,
        step=0.05,
        key="presidio_high_threshold",
    )

    texto_sim_exposto = (
        "Cliente Eduardo Pereira Silva (Curitiba) enviou o e-mail "
        "carlos.pereira@exemplo.com.br, CPF 123.456.789 10 e cartão "
        "4095 2609 9393 4932. Código da catraca: 1234 5678."
    )
    texto_sim_protegido = (
        "Cliente [PERSON] ([LOCATION]) enviou o e-mail "
        "[EMAIL_ADDRESS], CPF ***.***.*** 10 e cartão "
        "**** **** **** 4932. Código da catraca: 1234 5678."
    )

    deck.compare_toggle(
        "Original (Exposto)",
        lambda: deck.highlighted_text(
            texto_sim_exposto,
            spans=_highlight_terms(
                texto_sim_exposto,
                (
                    ("Eduardo Pereira Silva", "PERSON"),
                    ("Curitiba", "LOCATION"),
                    ("carlos.pereira@exemplo.com.br", "EMAIL_ADDRESS"),
                    ("123.456.789 10", "CPF"),
                    ("4095 2609 9393 4932", "CREDIT_CARD"),
                    ("1234 5678", "POSSIBLE_ID"),
                ),
                (0.85, 0.72, 0.99, 0.90, 0.90, 0.41),
                high_threshold=limiar_alto,
            ),
            border="none",
        ),
        "Anonimizado (Protegido)",
        lambda: deck.highlighted_text(
            texto_sim_protegido,
            spans=_highlight_terms(
                texto_sim_protegido,
                (
                    ("[PERSON]", "CENSURA"),
                    ("[LOCATION]", "CENSURA"),
                    ("[EMAIL_ADDRESS]", "CENSURA"),
                    ("***.***.*** 10", "MÁSCARA"),
                    ("**** **** **** 4932", "MÁSCARA"),
                ),
                HighlightLevel.HIGH,
            ),
            border="none",
        ),
        title="Antes vs. Depois no Atendimento",
        kicker="Comparativo",
        key="sim_compare",
    )

    def _preview_operador(
        texto: str,
        termos: tuple[tuple[str, str], ...],
        nivel: HighlightLevel,
    ):
        return lambda: deck.highlighted_text(
            texto,
            spans=_highlight_terms(texto, termos, nivel),
            border="none",
        )

    operadores_demo = (
        (
            "Censura Direta",
            "A paciente [PESSOA] pagou a consulta com o cartão final [NUMERO].",
            (("[PESSOA]", "CENSURA"), ("[NUMERO]", "CENSURA")),
            HighlightLevel.LOW,
        ),
        (
            "Mascaramento",
            "A paciente M**** da S**** pagou a consulta com o cartão final 1***.",
            (("M**** da S****", "MÁSCARA"), ("1***", "MÁSCARA")),
            HighlightLevel.LOW,
        ),
        (
            "Hash",
            "A paciente 8f2a1b pagou a consulta com o cartão final a7b9c1.",
            (("8f2a1b", "HASH"), ("a7b9c1", "HASH")),
            HighlightLevel.LOW,
        ),
        (
            "Pseudonimização",
            "A paciente Carla Mendes pagou a consulta com o cartão final 9876.",
            (("Carla Mendes", "PSEUDÔNIMO"), ("9876", "PSEUDÔNIMO")),
            HighlightLevel.HIGH,
        ),
    )

    deck.step_tabs(
        [
            (rotulo, _preview_operador(texto_op, termos_op, nivel_op))
            for rotulo, texto_op, termos_op, nivel_op in operadores_demo
        ],
        title="Operadores Aplicados ao Mesmo Registro",
        kicker="Simulador",
        key="sim_operators",
    )

    # 5.2 Quiz de Fixação
    deck.topic("5.2 ) Quiz de Fixação")
    deck.quiz(
        "Qual técnica de anonimização permite cruzar registros entre tabelas diferentes sem revelar o dado original?",
        [
            "Censura Direta ([PESSOA])",
            "Criptografia Irreversível (Hash)",
            "Mascaramento Parcial com asteriscos",
        ],
        answer_index=1,
        explanation=(
            "Entradas idênticas geram sempre o mesmo código hash, permitindo "
            "relacionar chaves entre tabelas sem expor a identidade real."
        ),
        title="Questão 01 — Técnicas de Anonimização",
        key="quiz_q1_hash",
    )

    deck.quiz(
        "Qual componente do Microsoft Presidio permite cadastrar regras customizadas com regex (como CPF ou TICKET-1234)?",
        [
            "AnonymizerEngine",
            "PatternRecognizer",
            "ImagePiiVerifyEngine",
        ],
        answer_index=1,
        explanation=(
            "O PatternRecognizer encapsula padrões Pattern (regex e score) "
            "registrados no AnalyzerEngine para formatos específicos do negócio."
        ),
        title="Questão 02 — Regras Customizadas",
        key="quiz_q2_pattern",
    )

    deck.quiz(
        "Por que revisar entidades detectadas com pontuação (score) baixa antes de bloquear automaticamente um texto?",
        [
            "Para evitar falsos positivos em números comuns, como códigos internos ou senhas de acesso.",
            "Porque o AnonymizerEngine ignora entidades com score acima de 0.75.",
            "Para converter exames DICOM em planilhas CSV.",
        ],
        answer_index=0,
        explanation=(
            "Pontuações baixas sinalizam baixa confiança (como um código de catraca "
            "confundido com cartão); calibrar o limiar evita bloqueios indevidos."
        ),
        title="Questão 03 — Falsos Positivos e Calibração",
        key="quiz_q3_score",
    )

    deck.quiz_summary(title="Placar Final da Apresentação")

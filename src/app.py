"""Apresentação sobre o Microsoft Presidio construída com pystslides."""

from pystslides import (
    HighlightLevel,
    HighlightSpan,
    Presentation,
    PresentationTheme,
    get_editorial_assets_dir,
)


def _highlight_terms(
    text: str,
    terms: tuple[tuple[str, str], ...],
    level: HighlightLevel,
) -> list[HighlightSpan]:
    """Localiza trechos no texto e constrói os `HighlightSpan` correspondentes."""
    spans: list[HighlightSpan] = []
    for term, label in terms:
        start = text.index(term)
        spans.append(HighlightSpan(start, start + len(term), label, level=level))
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

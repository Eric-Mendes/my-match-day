import streamlit as st
from datetime import timedelta
import pandas as pd
from app.schedule import make_schedule


def main():
    st.set_page_config(
        page_title="My Match Day - Crie um cronograma do brasileirão que atenda as suas necessidades",
        page_icon=":soccer:"
    )

    st.title("My Match Day - Crie um cronograma do brasileirão que atenda as suas necessidades")
    st.write("Você só tem o domingo à tarde pra ir ao estádio mas só descobre que vai ter jogo na madrugada de sábado pra domingo? \
             Este app lista todos os próximos jogos já com horário definido que são de algum time específico, em algum ou alguns estádio(s), \
             em algum ou alguns dia(s) da semana, e que comecem antes de um determinado horário máximo. Você pode ver os jogos que respeitem sua rotina até 1 mês pra frente pra poder se preparar e ficar ligado pra comprar os ingressos.")
    team = st.selectbox(
        "Time", 
        ['Cuiabá', 'Flamengo', 'Botafogo', 'Corinthians', 'Bahia', 
         'Fluminense', 'Vasco', 'Palmeiras', 'São Paulo', 'Santos', 
         'Bragantino', 'Atlético-MG', 'Cruzeiro', 'Grêmio', 'Internacional', 
         'Goiás', 'Athlético-PR', 'Coritiba', 'América-MG', 'Fortaleza'], placeholder="Escolha times que você deseja acompanhar")

    stadiums = st.multiselect(
        "Estádios", 
        ['Alfredo Jaconi', 'Allianz Parque', 'Arena MRV', 'Arena Pantanal',
         'Arena da Baixada', 'Beira-Rio', 'Castelão (CE)', 'Couto Pereira',
         'Independência', 'Kleber Andrade', 'Maracanã', 'Mineirão', 'Nabi Abi Chedid',
         'Neo Química Arena', 'Nilton Santos (Engenhão)', 'Vila Belmiro'], placeholder="Escolha os estádios onde você deseja ir")
    
    weekdays = st.multiselect(
        "Dias da semana", 
        ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"], placeholder="Escolha os dias da semana que você topa ver jogo")
    
    time = st.time_input("Hora mais tarde que você aceita que um jogo comece", step=timedelta(minutes=30))

    generate_matches_schedule = st.button("Crie meu cronograma", use_container_width=True)
    if generate_matches_schedule:
        schedule = make_schedule(team=team, stadiums=stadiums, weekdays=weekdays, time=time)
        st.dataframe(schedule)
        schedule.to_csv("cronograma.csv", index=False)
        st.download_button("Salvar este cronograma", data="cronograma.csv")

    st.write("Isto é só uma prova de conceito. Se este gostarem deste app ele vira uma newsletter mais robusta. Mande uma mensagem no meu [LinkedIn](https://www.linkedin.com/in/eric-v-p-mendes/) dizendo o que achou!")
    st.markdown("Made with :heart: by [@Eric-Mendes](https://github.com/Eric-Mendes)")

if __name__ == "__main__":
    main()

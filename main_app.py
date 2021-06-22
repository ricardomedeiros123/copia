import streamlit as st
from streamlit.hashing import _CodeHasher
import quant_app_carteira
import quant_app_correlacao
#import quant_app_carteira2
#import quant_app_teste
import yfinance as yf
import investpy as inv
import pandas as pd
from datetime import datetime

try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server
    
st.set_option('deprecation.showPyplotGlobalUse', False) # Desabilitar os Warnigs sobre o Pyplot
st.set_page_config(page_title='Análise Quant', layout = 'wide', initial_sidebar_state = 'auto') # Configurar Pagina

def main():
    state = _get_state()

    #Removing and add pages 
    pages = {
        "Análise de Carteira": page_carteira,
        "Análise de Correlações": page_correlacao
        }  

    st.sidebar.title(":chart: Análise Quant v.2")
    page = st.sidebar.radio("Selecione a opção", tuple(pages.keys()))
    st.sidebar.markdown("***")
    st.sidebar.markdown('''<small>Criado por Roberto Martins</small>''', unsafe_allow_html=True)
    st.sidebar.markdown('''<small>rraires.dev@gmail.com</small>''', unsafe_allow_html=True)
    puxar_dados(state)

    ###### Iniciar o DataFrame do Portifolio, somente no primeiro carregamento da Página

    if state.controle == None:
      state.controle = "Teste"
      #st.write("Primeira vez") # Msg de controle do primeiro acessso
      state.portifolio = pd.DataFrame()
      state.portifolio['Ação'] = ''
      state.portifolio['Qtde'] = ''
      state.portifolio['Últ. Preço'] = ''
      state.portifolio['Valor na Carteira'] = ''
      #state.portifolio['%'] = ''
      state.portifolio['Setor'] = ''
      state.portifolio['SubSetor'] = ''
      state.portifolio['Beta do Ativo'] = ''
      #state.portifolio['Beta Ponderadorado'] = ''

    ##########################################


    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()

def page_carteira(state):
    quant_app_carteira.carteira(state)

def page_correlacao(state):
    quant_app_correlacao.correlacao(state)

def page_teste(state):
    quant_app_teste.teste(state)

def puxar_dados(state):
  stocks_list = inv.get_stocks_list(country='Brazil') #Pegar a lista das Ações Brasileiras
  stocks_list.remove('NATU3')
  stocks_list.append('NTCO3')
  stocks_list.append('BOVA11')
  #stocks_df = pd.DataFrame(stocks_list) #Transforma a lista em DataFrame
  #stocks_df.columns = ['Ticker'] #Adiciona o nome da coluna
  #indices = [{'Ticker': 'Indice Bovespa'}, {'Ticker': 'Indice Dolar'},{'Ticker': 'Indice SP500'}, {'Ticker': 'Indice Dow Jones'}, {'Ticker': 'Indice NASDAQ'}]
  #stocks_df = stocks_df.append(indices, ignore_index=True)
  #state.stocks_df = stocks_df.sort_values(by='Ticker').reset_index(drop=True) #Ordena por ordem alfabetica e reseta o index
  state.stocks_df = stocks_list


######### Área da Persistencia de Sessão #########

class _SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)
        
    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value
    
    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()
    
    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False
        
        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state
##############################################

if __name__ == "__main__":
    main()
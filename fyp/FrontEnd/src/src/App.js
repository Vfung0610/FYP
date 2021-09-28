import "./App.css";
import SearchBar from "./SearchBar/SearchBar";
import GrpSearchResult from "./GrpSearchResult/GrpSearchResult";
import { getSubClass, searchQuery } from "./API/APIFunction";
import { useReducer } from "react";

//Reducer used for react to different action of the website
const reducer = (state, action) => {
  switch (action.type) {
    case "LOAD_START":
      return { ...state, loading: true };

    case "LOAD_FINISH":
      return { ...state, loading: false };

    case "REFRESH_RESULT":
      return { ...state, searchResult: action.result };

    case "REFRESH_ADVANCESEARCH":
      return { ...state, advanceResult: action.advanceResult };

    case "SEARCH_SUBCLASS":
      return {
        loading: false,
        searchDefaultText: action.newSearchText,
        searchResult: {},
        advanceSearch: {},
        pageNo: 0,
      };

    case "DOMAIN_NEXT_PAGE":
      return { ...state, pageNo: state.pageNo + 1 };

    case "DOMAIN_PREVIOUS_PAGE":
      return { ...state, pageNo: state.pageNo - 1 };

    default:
      return state;
  }
};

const defaultstate = {
  loading: false,
  searchDefaultText: "",
  searchResult: {},
  advanceSearch: {},
  pageNo: 0,
};

//Main App
function App() {
  const [state, dispatch] = useReducer(reducer, defaultstate);

  //function to perform search
  const search = async (query) => {
    dispatch({ type: "LOAD_START" });
    const result = await searchQuery(query);
    dispatch({ type: "LOAD_FINISH" });
    dispatch({ type: "REFRESH_RESULT", result: result });
  };

  //function to get subDomain specific knowledge
  const getOntology = async (query) => {
    dispatch({ type: "LOAD_START" });
    const result = await getSubClass(query);
    dispatch({ type: "LOAD_FINISH" });
    dispatch({ type: "REFRESH_ADVANCESEARCH", advanceResult: result });
  };

  //function to search for activate search for subDomain spedific knowledge
  const searchSubClass = async (keyword) => {
    dispatch({ type: "SEARCH_SUBCLASS", newSearchText: keyword });
    const result = await getOntology(keyword);
  };

  return (
    <div className="App">
      <header className="App-header">
        {state.loading && <div className="statusBox">Searching...</div>}
        <SearchBar
          searchDefaultText={state.searchDefaultText}
          search={search}
          getOntology={getOntology}
          advanceResult={state.advanceResult}
        />
        {
          //show search result if it exist
          state.searchResult &&
            Object.entries(state.searchResult).map((conceptObj) => {
              return (
                <div>
                  <GrpSearchResult
                    type="domain"
                    result={{
                      keyword: conceptObj[0],
                      result: conceptObj[1]["result"],
                    }}
                    pageNo={state.pageNo}
                    previousPage={() => {
                      dispatch({ type: "DOMAIN_PREVIOUS_PAGE" });
                    }}
                    nextPage={() => {
                      dispatch({ type: "DOMAIN_NEXT_PAGE" });
                    }}
                  />
                  {conceptObj[1]["subDomain"] && (
                    <div className="subDomainResultWrapper">
                      {conceptObj[1]["subDomain"].map((subClassObj) => {
                        return (
                          <GrpSearchResult
                            type="subDomain"
                            result={subClassObj}
                            searchMore={searchSubClass}
                          />
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })
        }
      </header>
    </div>
  );
}

export default App;

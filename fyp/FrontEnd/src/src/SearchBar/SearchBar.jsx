import "./SearchBar.css";
import { BsSearch } from "react-icons/bs";
import { useEffect, useState } from "react";

const SearchBar = ({
  search,
  searchDefaultText,
  getOntology,
  advanceResult,
}) => {
  const [searchTxt, setSearchTxt] = useState("");
  const [advanceSearchResult, setAdvanceSearchResult] = useState({});

  //function to get sub domain knowledge for searched keyword
  const searchBarSub = (e) => {
    e.preventDefault();

    if (searchTxt.trim() !== "") {
      getOntology(searchTxt);
    }
  };

  //function to get all search result for search keyword and selected sub domain specific knowledge
  const advanceSearchSub = (e) => {
    e.preventDefault();

    console.log(advanceSearchResult);
    search(advanceSearchResult);
  };

  //if list of sub domain knowledge is received, then show on page
  useEffect(() => {
    let tmpAdvanceResultObject = {};
    for (const item in advanceResult) {
      tmpAdvanceResultObject = { [item]: {} };
      advanceResult[item].forEach((obj) => {
        tmpAdvanceResultObject[item][obj] = false;
      });
    }
    //console.log(tmpAdvanceResultObject);
    tmpAdvanceResultObject["documentType"] = { all: true, article: true };
    setAdvanceSearchResult(tmpAdvanceResultObject);
  }, [advanceResult]);

  //set search bar default search text
  useEffect(() => {
    setSearchTxt(searchDefaultText);
  }, [searchDefaultText]);

  return (
    <div>
      <div className="searchBar">
        <form onSubmit={searchBarSub}>
          <input
            type="text"
            className="searchTxtInput"
            name="searchTxtInput"
            value={searchTxt}
            onChange={(e) => {
              setSearchTxt(e.target.value);
            }}
          />
          <button className="submitButton" type="submit">
            <BsSearch size={45} />
          </button>
        </form>
      </div>
      {
        //show list of sub domain knowledge with checkbox on screen if list of sub domain knowledge exists
        advanceResult && (
          <form onSubmit={advanceSearchSub}>
            <div className="advanceSearch">
              {Object.entries(advanceResult).map(([key, value]) => {
                return (
                  <div key={key}>
                    <div className="domainKnowledge">{key}</div>
                    {value.map((subClass) => {
                      return (
                        <label key={subClass}>
                          <input
                            type="checkbox"
                            value={subClass}
                            onChange={(e) => {
                              setAdvanceSearchResult({
                                ...advanceSearchResult,
                                [key]: {
                                  ...advanceSearchResult[key],
                                  [e.target.value]: !advanceSearchResult[key][
                                    e.target.value
                                  ],
                                },
                              });
                            }}
                          />
                          {subClass}
                        </label>
                      );
                    })}
                  </div>
                );
              })}
              <div className="advanceSearchType">
                <div>Search Type</div>
                {Object.entries(advanceSearchResult["documentType"]).map(
                  (item) => {
                    return (
                      <label key={item}>
                        <input
                          type="checkbox"
                          value={item}
                          checked={item[1]}
                          onChange={(e) => {
                            setAdvanceSearchResult({
                              ...advanceSearchResult,
                              documentType: {
                                ...advanceSearchResult["documentType"],
                                [item[0]]: !item[1],
                              },
                            });
                          }}
                        />
                        {item}
                      </label>
                    );
                  }
                )}
              </div>
              <button className="advanceSearchButton" type="submit">
                Search
              </button>
            </div>
          </form>
        )
      }
    </div>
  );
};

export default SearchBar;

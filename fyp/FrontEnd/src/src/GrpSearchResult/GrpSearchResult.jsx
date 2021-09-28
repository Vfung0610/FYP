import "./GrpSearchResult.css";
import SearchResult from "../SearchResult/SearchResult";
import { BsArrowBarLeft, BsArrowBarRight } from "react-icons/bs";

const GrpSearchResult = (prop) => {
  return (
    <div
      className={
        //different class name for css use to format domain and sub domain search result
        prop.type === "domain"
          ? "GrpSearchResult_Main"
          : "GrpSearchResult_Other"
      }
    >
      <h2>{prop.result["keyword"]}</h2>
      {
        //domain keyword search result
        prop.type === "domain" &&
          prop.result["result"] &&
          prop.result["result"]
            .slice(0 + 10 * prop.pageNo, 0 + 10 * prop.pageNo + 10)
            .map((resultObj) => {
              return <SearchResult key={resultObj["id"]} {...resultObj} />;
            })
      }
      {
        //sub domain search result
        prop.type === "subDomain" &&
          prop.result["result"].map((resultObj) => {
            return <SearchResult key={resultObj["id"]} {...resultObj} />;
          })
      }
      {
        //if domain keyword, add previous/next page. If not, add search more button for sub domain knowledge search result
        prop.type === "domain" ? (
          <div className="navPage">
            {prop.pageNo > 0 && (
              <BsArrowBarLeft size={30} onClick={prop.previousPage} />
            )}
            {prop.pageNo < 9 && (
              <BsArrowBarRight
                onClick={prop.nextPage}
                className="NextPage"
                size={30}
              />
            )}
          </div>
        ) : (
          <div className="ShowMoreIcon">
            <button
              onClick={() => {
                prop.searchMore(prop.result["keyword"]);
              }}
            >
              Search More
            </button>
          </div>
        )
      }
    </div>
  );
};

export default GrpSearchResult;

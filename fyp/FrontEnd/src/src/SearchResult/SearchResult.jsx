import "./SearchResult.css";

const SearchResult = ({ link, title, summary }) => {
  return (
    <div className="searchResult">
      <a href={link}>{title}</a>
      <p>{summary}</p>
    </div>
  );
};

export default SearchResult;

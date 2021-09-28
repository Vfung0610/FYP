//function to perform action search after subDomain knowledge is selected
export const searchQuery = async (query) => {
  //console.log(JSON.stringify({ data: query }));
  const response = await fetch("http://localhost:5000/api/search/", {
    body: JSON.stringify({ data: query }),
    cache: "no-cache",
    headers: {
      "content-type": "application/json",
    },
    method: "POST",
  });
  const result = await response.json();
  //console.log(result);
  return result;
};

//function to get sub domain knowledge of searched keyword
export const getSubClass = async (query) => {
  const response = await fetch(
    "http://localhost:5000/api/getOntology/" + query
  );
  const result = await response.json();
  //console.log(result);
  return result;
};

import "./styles.css";
import Cite from "citation-js";
require("@citation-js/plugin-bibtex");
require("@citation-js/plugin-ris");

export default function App() {
  const bibliographyData = [
    {
      id: "Q23571040",
      type: "article-journal",
      title: "Correlation of the Base Strengths of Amines 1",
      DOI: "10.1021/ja01577a030",
      author: [
        {
          given: "H. K.",
          family: "Hall"
        }
      ],
      issued: { "date-parts": [[1957, 1, 1]] },
      "container-title": "Journal of the American Chemical Society",
      volume: "79",
      issue: "20",
      page: "5441-5444"
    }
  ];

  const reference = new Cite(bibliographyData);

  return (
    <div className="App">
      <h1>Test citation-js</h1>
      <hr />
      {["html", "text"].map((format) => {
        const refs = {
          citation: reference.format("citation", {
            template: "apa",
            format
          }),
          bibliography_apa: reference.format("bibliography", {
            template: "apa",
            format
          }),
          bibliography_vancouver: reference.format("bibliography", {
            template: "vancouver",
            format
          }),
          bibliography_harvard1: reference.format("bibliography", {
            template: "harvard1",
            format
          }),
          bibtex: reference.format("bibtex", {
            format
          }),
          biblatex: reference.format("biblatex", {
            format
          }),
          bibtxt: reference.format("bibtxt", {
            format
          }),
          ris: reference.format("ris", {
            format
          })
        };

        return (
          <>
            <h2>■{format}</h2>
            {Object.entries(refs).map(([key, value]) => {
              return (
                <>
                  <h3>・{key}</h3>
                  <p dangerouslySetInnerHTML={{ __html: value }} />
                </>
              );
            })}
            <hr />
          </>
        );
      })}
    </div>
  );
}

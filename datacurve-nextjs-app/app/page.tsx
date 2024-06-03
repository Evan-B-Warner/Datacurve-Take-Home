import Editor from '../components/CodeEditor';

export default function Home() {
  return (
    <body>
      <h2>Python Code Editor</h2>
      <div className="editor h-full">
        <div className="left">
          <p>Code:</p>
          <Editor />
        </div>
        <div className="right">
          <div className="topright">
            <p>stdout</p>
            <p id="codeOutput"></p>
          </div>
          <div className="topleft">
            <p>stderr</p>
            <p id="codeError"></p>
          </div>
        </div>
      </div>
    </body>
  );
}

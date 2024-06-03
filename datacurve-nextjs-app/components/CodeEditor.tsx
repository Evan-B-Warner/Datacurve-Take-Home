'use client';

import React, { useState } from 'react';
import CodeEditor from '@uiw/react-textarea-code-editor';
import axios from 'axios';

export default function Editor() {
  const [code, setCode] = useState(`print("hello world")`);

  const runCode = async () => {
    const codeText = code;
    // run code and return stdout and stderr
    try {
      const response = await axios.post('http://127.0.0.1:8000/run_code', {
        code: codeText,
      });
      var codeOutput = document.getElementById('codeOutput');
      codeOutput.textContent = response.data.stdout;
      var codeError = document.getElementById('codeError');
      codeError.textContent = response.data.stderr;
      console.log(response);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const submitCode = async () => {
    const codeText = code;
    // attempt to save submission to database
    try {
      const response = await axios.post('http://127.0.0.1:8000/submit_code', {
        code: codeText,
      });
      console.log(response.data);
      if (response.data.saved) {
        alert('Code submission successfully saved!');
      } else {
        alert('Code resulted in errors, did not save!');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <main>
      <CodeEditor
        value={code}
        language="python"
        placeholder="Write your Python code here."
        onChange={evn => setCode(evn.target.value)}
        padding={15}
        style={{
          backgroundColor: '#f5f5f5',
          fontFamily:
            'ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace',
        }}
      />
      <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"
        rel="stylesheet"
      ></link>
      <div className="button-div"></div>
      <button
        className="btn btn-primary"
        style={{ marginLeft: '10px', marginRight: '10px', marginTop: '10px' }}
        onClick={runCode}
      >
        Test Code
      </button>
      <button
        className="btn btn-success"
        style={{ marginTop: '10px' }}
        onClick={submitCode}
      >
        Submit
      </button>
    </main>
  );
}

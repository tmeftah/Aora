const inputField = document.getElementById('input-field');
const sendButton = document.getElementById('send-button');
const outputField = document.getElementById('output-field');

sendButton.addEventListener('click', () => {
  const question = inputField.value;
  const url = 'http://127.0.0.1:8000/query';
  const queryParam = `query=${question}`;

  fetch(`${url}?${queryParam}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      } else {
        return response.body.getReader();
      }
    })
    .then(reader => {
      let text = '';
      function readChunk(reader) {
        reader.read().then(({ done, value }) => {
          if (done) {
            console.log('All chunks processed.');
            
            return;
          }

          const chunkText = new TextDecoder('utf-8').decode(value);
          text += chunkText;
          console.log('Chunk received:', chunkText);
          outputField.value = text;

          readChunk(reader); // Loop to read the next chunk
        });
      }

      readChunk(reader);
    })
    .catch(error => console.error('Error fetching the data:', error));
});
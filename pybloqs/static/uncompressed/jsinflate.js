(function(){
  function decompress(bytes) {
  const input = new ReadableStream({
    start(c) {
      c.enqueue(bytes);
      c.close();
    },
  }).pipeThrough(new DecompressionStream("deflate"));

  const reader = input.getReader();
  const chunks = [];

  return reader.read().then(function process({ done, value }) {
    if (done) {
      const decompressedData = new Uint8Array(
        chunks.reduce((acc, chunk) => acc + chunk.length, 0)
      );
      let offset = 0;
      chunks.forEach(chunk => {
        decompressedData.set(chunk, offset);
        offset += chunk.length;
      });
      return decompressedData;
    }
    chunks.push(value);
    return reader.read().then(process);
  });
}

var zip_inflate=async function(str){
  const binaryString = atob(str);
  var bytes = new Uint8Array(binaryString.length);
  for (var i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
  }
  return decompress(bytes)
    .then(decompressed => (new TextDecoder().decode(decompressed)))
    .catch(console.error);
}
if(!window.RawDeflate)RawDeflate={};RawDeflate.inflate=zip_inflate;}
)();

function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


function dropDownElementSelect(e){

    console.log("This is working")
    document.getElementById("category").value = e.target.value
}

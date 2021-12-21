function deleteNote(noteId) {
  if (confirm("Do you want to delete this note?")) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }
}

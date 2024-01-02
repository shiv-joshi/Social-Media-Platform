function deletePost(postId) {
    // send POST request with postId
    fetch('/delete-post', {
        method: 'POST',
        body: JSON.stringify({ postId: postId }), // turns it into a string
    }).then((_res) => { 
        // after you get a response, reload page to homepage
        window.location.href = "/"; 
    });
}

function editPost(postId, newText) {
    fetch('/edit-post', {
        method: 'POST',
        body: JSON.stringify({ postId: postId, newText: newText }),
    }).then((_res) => { 
        window.location.href = "/"; 
    });
}

function addComment(postId, commentText) {
    fetch('/add-comment', {
        method: 'POST',
        body: JSON.stringify({ postId: postId, commentText: commentText }),
    }).then((_res) => { 
        window.location.href = "/"; 
    });
}
function handleSortChange(select) {
    const sort = select.value;
    const category = new URLSearchParams(window.location.search).get("category");
    window.location.href = queryLogic(category,sort)
  }

  function handleCategoryChange(select) {
    const category = select.value;
    const sort = new URLSearchParams(window.location.search).get("sort");
    window.location.href = queryLogic(category,sort)
    
  }

  function queryLogic(category,sort){
    if (sort && category) { 
      return "?category="+category+"&sort="+sort
    }
    else if(sort){
      return "?sort="+ sort;
    }
    else if(category){
      return "?category="+category
    }
    else  return "/"
  }

function toggleFollow(button,authorId,csrfToken){
fetch(`/follow/author/${authorId}`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
       if (data.status =="followed")
        button.textContent = "Following"
       else if (data.status == "unfollowed")
        button.textContent = "Follow"
      else
        alert(data.message)
  })
  }
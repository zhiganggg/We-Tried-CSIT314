function shortlist(listingId) {
  const shortlistCount = document.getElementById(
    `shortlists-count-${listingId}`
  );
  const shortlistButton = document.getElementById(
    `shortlist-button-${listingId}`
  );

  fetch(`/shortlist-listing/${listingId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      shortlistCount.innerHTML = data["shortlists"];
      if (data["shortlisted"] === true) {
        shortlistButton.className = "fa fa-heart";
      } else {
        shortlistButton.className = "fa fa-heart-o";
      }
    })
    .catch((e) => alert("Could not like post."));
}

document.getElementById("profile").addEventListener("change", function () {
  var agentFields = document.getElementById("agent-fields");
  var selectedRoleName = this.options[this.selectedIndex].text;
  if (selectedRoleName === "Agent") {
    agentFields.style.display = "block";
  } else {
    agentFields.style.display = "none";
  }
});

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
        shortlistButton.className = "btn btn-outline-secondary active";
      } else {
        shortlistButton.className = "btn btn-outline-secondary";
      }
    })
    .catch((error) => {
      console.error("Error posting shortlist:", error);
      alert("Could not shortlist listing. Please try again later.");
    });
}

function shortlist2(listingId) {
  const shortlistButton2 = document.getElementById(
    `shortlist-button2-${listingId}`
  );

  fetch(`/shortlist-listing/${listingId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      if (data["shortlisted"] === true) {
        shortlistButton2.innerHTML =
          '<i class="bi bi-heart-fill"></i> Unshortlist';
      } else {
        shortlistButton2.innerHTML = '<i class="bi bi-heart"></i> Shortlist';
      }
    })
    .catch((error) => {
      console.error("Error posting shortlist:", error);
      alert("Could not shortlist listing. Please try again later.");
    });
}

function calculateMortgage() {
  var propertyPrice = parseFloat(
    document.getElementById("property-price").value.replace(/,/g, "")
  );
  var loanAmount = parseFloat(
    document.getElementById("loan-amount").value.replace(/,/g, "")
  );
  var interestRate =
    parseFloat(document.getElementById("interest-rate").value) / 100;
  var loanTenure = parseInt(document.getElementById("loan-tenure").value);
  var principalBar = document.getElementById("principal-bar");
  var interestBar = document.getElementById("interest-bar");
  var downpaymentBar = document.getElementById("downpayment-bar");
  var loanBar = document.getElementById("loan-bar");

  var monthlyInterestRate = interestRate / 12;
  var numPayments = loanTenure * 12;

  //prettier-ignore
  var monthlyPayment =
    loanAmount *
    ((monthlyInterestRate * ((1 + monthlyInterestRate) ** numPayments)) /
      (((1 + monthlyInterestRate) ** numPayments) - 1));
  var monthlyInterest = loanAmount * monthlyInterestRate;
  var monthlyPrincipal = monthlyPayment - monthlyInterest;
  var downpaymentAmount = propertyPrice - loanAmount;

  var interestPercentage = (monthlyInterest / monthlyPayment) * 100;
  var principalPercentage = 100 - interestPercentage;

  var loanPercentage = Math.round((loanAmount / propertyPrice) * 100);
  var downpaymentPercentage = 100 - loanPercentage;

  document.getElementById("monthly-payment").innerText =
    "S$ " +
    monthlyPayment.toLocaleString(undefined, { maximumFractionDigits: 0 }) +
    " / mo";
  document.getElementById("monthly-interest").innerText =
    "S$ " +
    monthlyInterest.toLocaleString(undefined, { maximumFractionDigits: 0 }) +
    " Interest";
  document.getElementById("monthly-principal").innerText =
    "S$ " +
    monthlyPrincipal.toLocaleString(undefined, { maximumFractionDigits: 0 }) +
    " Principal";
  document.getElementById("downpayment-amt").innerText =
    "S$ " +
    downpaymentAmount.toLocaleString(undefined, { maximumFractionDigits: 0 });
  document.getElementById("loan-amt").innerText =
    "S$ " +
    loanAmount.toLocaleString(undefined, { maximumFractionDigits: 0 }) +
    " Loan";
  document.getElementById("interest-bar").innerText =
    interestPercentage.toLocaleString(undefined, { maximumFractionDigits: 0 }) +
    "%";
  document.getElementById("principal-bar").innerText =
    principalPercentage.toLocaleString(undefined, {
      maximumFractionDigits: 0,
    }) + "%";
  document.getElementById("loan-bar").innerText =
    loanPercentage.toLocaleString(undefined, { maximumFractionDigits: 0 }) +
    "%";
  document.getElementById("downpayment-bar").innerText =
    downpaymentPercentage.toLocaleString(undefined, {
      maximumFractionDigits: 0,
    }) + "%";
  interestBar.style.width =
    interestPercentage.toLocaleString(undefined, { maximumFractionDigits: 0 }) +
    "%";
  principalBar.style.width =
    principalPercentage.toLocaleString(undefined, {
      maximumFractionDigits: 0,
    }) + "%";
  loanBar.style.width =
    interestPercentage.toLocaleString(undefined, { maximumFractionDigits: 0 }) +
    "%";
  downpaymentBar.style.width =
    principalPercentage.toLocaleString(undefined, {
      maximumFractionDigits: 0,
    }) + "%";
}

$(document).ready(function () {
  $("#bedroomFilterBtn").click(function (event) {
    event.preventDefault();

    var formData = $("form").serialize();

    $.ajax({
      type: "GET",
      url: "/search-bedroom",
      data: formData,
      success: function (response) {
        $("#listings").html(response);
      },
      error: function (xhr, status, error) {
        console.error("Error:", error);
      },
    });
  });
});

$(document).ready(function () {
  $("#priceFilterForm").submit(function (event) {
    event.preventDefault();

    var minPrice = $("#minPriceInput").val();
    var maxPrice = $("#maxPriceInput").val();

    $.ajax({
      type: "GET",
      url: "/search-price",
      data: { min_price: minPrice, max_price: maxPrice },
      success: function (response) {
        $("#listings").html(response);
      },
      error: function (xhr, status, error) {
        console.error("Error:", error);
      },
    });
  });
});

$(document).ready(function () {
  $("#typeFilterBtn").click(function (event) {
    event.preventDefault();

    var formData = $("form").serialize();

    $.ajax({
      type: "GET",
      url: "/search-type",
      data: formData,
      success: function (response) {
        $("#listings").html(response);
      },
      error: function (xhr, status, error) {
        console.error("Error:", error);
      },
    });
  });
});

$(document).ready(function () {
  // Handle form submission on Enter key press
  $("#search").keypress(function (event) {
    if (event.keyCode === 13) {
      // Enter key code
      event.preventDefault();
      $("#searchForm").submit(); // Submit the form
    }
  });
});

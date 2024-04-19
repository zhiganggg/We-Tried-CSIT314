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
    .catch((e) => alert("Could not like post."));
}

function calculateMortgage() {
  var propertyPrice = parseFloat(
    document.getElementById("property-price").value
  );
  var loanAmount = parseFloat(document.getElementById("loan-amount").value);
  var interestRate =
    parseFloat(document.getElementById("interest-rate").value) / 100;
  var loanTenure = parseInt(document.getElementById("loan-tenure").value);
  var principalBar = document.getElementById("principal-bar");
  var interestBar = document.getElementById("interest-bar");
  var downpaymentBar = document.getElementById("downpayment-bar");
  var loanBar = document.getElementById("loan-bar");

  var monthlyInterestRate = interestRate / 12;
  var numPayments = loanTenure * 12;
  var monthlyPayment =
    loanAmount *
    ((monthlyInterestRate * (1 + monthlyInterestRate) ** numPayments) /
      ((1 + monthlyInterestRate) ** numPayments - 1));
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
    " Loan Amount";
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

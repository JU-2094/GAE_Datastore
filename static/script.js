// set a specific row to editMode or readMode
function toggleMode(target, currMode, destinationMode) {
  // find row to change
  var rowIdToEdit = target.dataset.id;

  // remove currMode class in target row
  document
    .getElementById("row-" + rowIdToEdit)
    .classList.remove("mode-" + currMode);

  // set destinationMode class in target row
  document
    .getElementById("row-" + rowIdToEdit)
    .classList.add("mode-" + destinationMode);

  if (currMode == "edit") savePayload(rowIdToEdit, updateCurrentRow);
}

// find row to edit
function updateCurrentRow(rowIdToEdit) {
  document.getElementById("read-location-" + rowIdToEdit).innerHTML =
    payload.location;
  document.getElementById("read-name-" + rowIdToEdit).innerHTML = payload.name;
  document.getElementById("read-address-" + rowIdToEdit).innerHTML =
    payload.address;
  document.getElementById("read-polarity-" + rowIdToEdit).innerHTML =
    payload.polarity;
  document.getElementById("read-category-" + rowIdToEdit).innerHTML =
    payload.category;
  document.getElementById("read-subcategory-" + rowIdToEdit).innerHTML =
    payload.subcategory;
  document.getElementById("read-lat-" + rowIdToEdit).innerHTML = payload.lat;
  document.getElementById("read-lng-" + rowIdToEdit).innerHTML = payload.lng;
}

// close  `addNewLocation` row
function closeIfsuccess() {
  location.reload();
  // document.getElementById("newPlace").classList.remove("edit");
  // document.getElementById("newPlace").classList.add("read");
}

// save edited/created data using callback to handle `edit` and `createNew` cases
function savePayload(rowIdToEdit = null, callback) {
  // get all input data
  if (rowIdToEdit) {
    payload = {
      location: document.getElementById("location-" + rowIdToEdit).value,
      name: document.getElementById("name-" + rowIdToEdit).value,
      address: document.getElementById("address-" + rowIdToEdit).value,
      polarity: document.getElementById("polarity-" + rowIdToEdit).value,
      category: document.getElementById("category-" + rowIdToEdit).value,
      subcategory: document.getElementById("subcategory-" + rowIdToEdit).value,
      lat: document.getElementById("lat-" + rowIdToEdit).value,
      lng: document.getElementById("lng-" + rowIdToEdit).value,
    };
  } else {
    payload = {
      location: document.getElementById("new_location").value,
      name: document.getElementById("new_name").value,
      address: document.getElementById("new_address").value,
      polarity: document.getElementById("new_polarity").value,
      category: document.getElementById("new_category").value,
      subcategory: document.getElementById("new_subcategory").value,
      lat: document.getElementById("new_lat").value,
      lng: document.getElementById("new_lng").value,
    };
  }

  // send payload to backend
  var xmlHttp = new XMLHttpRequest();
  var addUrl = "/add_location";
  var editUrl = "/edit/" + rowIdToEdit;

  xmlHttp.open("POST", rowIdToEdit ? editUrl : addUrl);
  xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

  xmlHttp.onreadystatechange = function () {
    if (xmlHttp.readyState === 4 && xmlHttp.status == 202) {
      if (rowIdToEdit) {
        callback(rowIdToEdit); // any function to pass as argument like closures
      } else {
        callback();
      }
    }
  };

  xmlHttp.send(JSON.stringify(payload));
}

// function to enable `add a new location` feature
function showAddRow() {
  document.getElementById("newPlace").classList.remove("read");
  document.getElementById("newPlace").classList.add("edit");
}

// function to save and disable `add a new location` feature if successful
function hideAddRow() {
  savePayload(null, closeIfsuccess);
}

// apply filters search feature, send query string to backend
function applyFilters() {
  var xmlHttp = new XMLHttpRequest();

  var params = {
    loc_f: document.getElementById("loc_f").value,
    name_f: document.getElementById("name_f").value,
    pol_min: document.getElementById("pol_min").value,
    pol_max: document.getElementById("pol_max").value,
    cat_f: document.getElementById("cat_f").value,
    subcat_f: document.getElementById("subcat_f").value,
  };

  var searchParams = new URLSearchParams();

  Object.keys(params).forEach((element) => {
    searchParams.append(element, params[element]);
  });

  var query = searchParams.toString();

  console.log("QUERY FILTERS " + query);
  var filtersUrl = "/apply_filter?" + query;

  window.open("https://norse-block-301718.uc.r.appspot.com"+filtersUrl,"_self");
  //xmlHttp.open("POST", filtersUrl, true);

  //xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

  //xmlHttp.onreadystatechange = function () {
  //  if (xmlHttp.readyState === 4 && xmlHttp.status == 202) {
  //    console.log(xmlHttp.responseText);
  //  }
  //};

  //console.log("before sending");
  //xmlHttp.send(filtersUrl);
  //console.log("After sending");
}

// retrieves the next 10 results in the table
// after clicking next Page button
function nextPage() {}

// get reviews after selecting a location
function showReview(target) {
  var rowToShow = target.id;
  var reviewsToShow = document.querySelectorAll(".card-wrapper");

  // logic to find a match with clicked row and reviews for that row
  reviewsToShow.forEach((review) => {
    if (review.classList.contains(rowToShow)) {
      review.classList.remove("hidden");
    } else {
      // no son parte de mi row, ocultar
      if (!review.classList.contains("hidden")) {
        review.classList.add("hidden");
      }
    }
  });
}

// add a review to a specific location
function getRowAddReview(target, rowNum) {
  rowToAddReviewTo = rowNum;
  var modal = document.getElementById("addReview");
  modal.classList.add("is-active");
  modal.dataset.row = rowNum;
}

// close modal when onclick on cancel button in modal
function closeModal() {
  var modal = document.getElementById("addReview");
  modal.classList.remove("is-active");
}

// saves review in backend from user review input
function saveReview(target) {
  closeModal();
  location.reload();

  var rowToChange = parseInt(document.getElementById("addReview").dataset.row);
  reviewPayload = {
    reviewText: document.getElementById("form_text").value,
    reviewRating: document.getElementById("form_rating").value,
  };

  var xmlHttp = new XMLHttpRequest();
  var addReviewURl = "/add_review/" + rowToChange;

  xmlHttp.open("POST", addReviewURl, true);
  xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

  xmlHttp.onreadystatechange = function () {
    if (xmlHttp.readyState === 4 && xmlHttp.status == 202) {
      alert(xmlHttp.responseText);
    }
  };

  xmlHttp.send(JSON.stringify(reviewPayload));
}

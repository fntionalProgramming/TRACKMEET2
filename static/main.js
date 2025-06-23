const TRACK_DATA = "track_meet_data";
/*
this function will take a string in then clean all alhanumeric characters of it
*/
function clean_string(str) {
  return str.replace(/[^a-zA-Z0-9\s]/g, "").trim();
}

function update_count(entries_amount, count_id = "Count") {
  count = document.getElementById(count_id);
  count.textContent = `Entries: ${entries_amount}`;
}
/*
this function will take the meets info 
then return all the lsit of unique shcool for later sorting
*/
function get_school_event_category(meets_info) {
  // init a set since it removes duplicates
  let schools = new Set();
  let events = new Set();
  let categories = new Set();
  meets_info.forEach((meet) => {
    // remove the header
    meet = meet[1].slice(1);
    meet.forEach((row) => {
      // now extract the school from the row
      // row -> "Adebiyi, Kin",Intermediate,TDC,NT,Male 100m, ,male,100m, ,Track
      const school = row.split(",")[3].trim();
      const event = row.split(",")[5].trim();
      const category = row.split(",")[2].trim();
      // shcool also will always exits so we do not need any check for if it not exits
      schools.add(school);
      events.add(event);
      categories.add(category);
    });
  });
  // conver the set into an array
  schools = Array.from(schools);
  // sort the school and in javascript sort wil automatically infer type so this sort will sort by alphabetically
  schools = schools.sort();

  // do the samething for the events
  events = Array.from(events);
  events = events.sort();

  // do also the samething for categories
  categories = Array.from(categories);
  categories = categories.sort();
  return { schools, events, categories };
}
/*
this function will sort each rows by school
*/
function update_schoolevent_filter(
  status_text_id = "StatusText",
  sort_by_button_id = "SortBySchool",
  sort_by_event_id = "SortByEvent",
  sort_by_category_id = "SortByCategory"
) {
  // get the sort button
  const sort_event_button = document.getElementById(sort_by_event_id);
  const sort_category_button = document.getElementById(sort_by_category_id);
  const sort_button = document.getElementById(sort_by_button_id);
  // start by getting the track data from local storage
  const track_data = localStorage.getItem(TRACK_DATA);
  const status_text = document.getElementById(status_text_id);
  // track data should also exits so if it doesnot something went wwrong
  if (!track_data) {
    status_text.textContent =
      "Cannot find trakc data something is wrong please try to refresh your browser or restart the application";
    status_text.style.color = "red";
    return;
  }
  // parse the meets info, get the list of schools
  const meets_info = JSON.parse(track_data);
  let { schools, events, categories } = get_school_event_category(meets_info);
  // update the sort button based on the schools retrives
  // clear the previous options
  sort_button.innerHTML = "";
  // give the use a default option
  sort_button.innerHTML = '<option value="">All</option>';
  schools.forEach((school) => {
    // create a new option element then assign the appropriate value and text content then append it
    const option = document.createElement("option");
    option.value = school;
    option.textContent = school;
    sort_button.appendChild(option);
  });

  // now to the samething for the event_filter
  sort_event_button.innerHTML = "";
  sort_event_button.innerHTML = '<option value="">All</option>';
  events.forEach((event) => {
    const option = document.createElement("option");
    option.value = event;
    option.textContent = event;
    sort_event_button.appendChild(option);
  });

  // now do also the samething for the category
  sort_category_button.innerHTML = "";
  sort_category_button.innerHTML = '<option value="">All</option>';
  categories.forEach((category) => {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    sort_category_button.appendChild(option);
  });
}

function add_choose_meets(
  status_text_id = "StatusText",
  choose_meet_id = "ChooseMeet",
  data_container_id = "DataContainer"
) {
  const data_container = document.getElementById(data_container_id);
  const status_text = document.getElementById(status_text_id);
  const choose_meet_select = document.getElementById(choose_meet_id);
  /*
    load data from the extracteed directories when the user clicks on the filter button
    */
  choose_meet_select.addEventListener("change", (event) => {
    const meet = event.target.value;
    // reset all of the other filter buttons again
    document.getElementById("SortBySchool").value = "";
    document.getElementById("SortByGender").value = "";
    document.getElementById("SortByType").value = "";
    document.getElementById("SearchInput").value = "";

    const track_data = localStorage.getItem(TRACK_DATA);
    if (!track_data) {
      status_text.textContent =
        "Cannnot find track data something is wrong please try to refresh your browser or restart the application";
      status_text.style.color = "red";
      return;
    }
    const meets_info = JSON.parse(track_data);
    // dispaly the meets info in the data container tab
    // first get what kind of meet is selected by the user
    const selected_meet = meets_info.find((m) => {
      return m[0].startsWith(meet);
    });

    if (!selected_meet) {
      status_text.textContent =
        "Selected meet not found in the data, Something went wrong please try to refresh your browser or restart the application or load the data again";
      status_text.style.color = "red";
      return;
    }

    // parse the csv files
    if (selected_meet[1].length === 0) {
      data_container.innerHTML = "<p>No data available for this meet.</p>";
      status_text.textContent =
        "No data available for this meet. Something went wrong please try to refresh your browser or restart the application";
      status_text.style.color = "red";
    }

    // get the header for the csv file
    const csv_header = selected_meet[1][0].split(",");
    // get all the rows except for the first one which is the hearer
    // then  split each data to an array value
    const csv_rows = selected_meet[1].slice(1).map((row) => {
      row = row.split(",");
      row[1] = row[0] + row[1]; // re add the first and last name of the athlete together
      row.shift(); // remove the first element since it is useless now
      return row;
    });
    // now since we got all the data we needed we can start by displaying in it through a html table
    let table = "<table style='width:100%; border-collapse: collapse;'>";
    // add in the header row
    table +=
      "<head><tr>" +
      csv_header
        .map((h) => `<th style='border:1px solid #ccc; padding:4px;'>${h}</th>`)
        .join("") +
      "</tr></thead>";
    table += "<tbody>";
    // now we can add in the rows
    csv_rows.forEach((row) => {
      table +=
        "<tr>" +
        row
          .map(
            (cell) =>
              `<td style='border:1px solid #ccc; padding:10px;'>${clean_string(
                cell
              )}</td>`
          )
          .join("") +
        "</tr>";
    });
    table += "</tbody></table>";
    data_container.innerHTML = table;

    update_schoolevent_filter();
    filter_and_render_table();
  });
}

function add_load_data_button(
  button_id = "LoadDataButton",
  status_text_id = "StatusText",
  load_data_event = "/load_data",
  choose_meet_id = "ChooseMeet"
) {
  const status_text = document.getElementById(status_text_id);
  const button = document.getElementById(button_id);
  button.addEventListener("click", () => {
    // herer display a wait button to the user first
    status_text.style.color = "black";
    status_text.style.visibility = "visible";
    status_text.textContent = "Fetching data ... (Might take a while)";
    fetch(load_data_event, { method: "POST" })
      .then((response) => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
      })
      .then((json) => {
        // all the data should be stored in the rolling_schedule directory so we can just retrive it later
        // before loading the data announce the user that the fetching of data is done
        status_text.textContent =
          "Done loading data, please now choose your kind of meets under the choose meet field";
        status_text.style.color = "green";
        // store the newly fetched data in the local storage
        localStorage.setItem(TRACK_DATA, JSON.stringify(json.meets_info));

        // update the options for the choose meet elements
        const choose_meet_select = document.getElementById(choose_meet_id);
        // clear the preivous options
        choose_meet_select.innerHTML = "";
        // for each element in the newly retrivre data make it a option
        json.meets_info.forEach((meet) => {
          const option = document.createElement("option");
          // get the value for the meet
          option.value = meet[0].split(" - ")[0];
          // get the text content ofthe meet
          option.textContent = meet[0];
          // finally adding the option
          choose_meet_select.appendChild(option);
        });
        update_schoolevent_filter();
        filter_and_render_table();
      })
      .catch((error) => {
        // here display the error button
        // announce the error
        status_text.textContent = "Error: " + error.message;
        status_text.style.color = "red";
      });
  });
}

function load_initial_data(choose_meet_id = "ChooseMeet") {
  const status_text = document.getElementById("StatusText");
  fetch("/load_initial_data", { method: "POST" })
    .then((response) => {
      if (!response.ok) throw new Error("Network response was not ok");
      return response.json();
    })
    .then((json) => {
      if (json.status === "unsuccessful") {
        status_text.innerHTML = json.error_message;
        return;
      }
      localStorage.setItem(TRACK_DATA, JSON.stringify(json.meets_info));
      const choose_meet_select = document.getElementById(choose_meet_id);
      // clear the preivous options
      choose_meet_select.innerHTML = "";
      // for each element in the newly retrivre data make it a option
      json.meets_info.forEach((meet) => {
        const option = document.createElement("option");
        // get the value for the meet
        option.value = meet[0].split(" - ")[0];
        // get the text content ofthe meet
        option.textContent = meet[0];
        // finally adding the option
        choose_meet_select.appendChild(option);
      });
      update_schoolevent_filter();
      filter_and_render_table();
    })
    .catch((error) => {
      // here display the error button
      // announce the error
      status_text.textContent = "Error: " + error.message;
      status_text.style.color = "red";
    });
}

function filter_and_render_table(
  choose_meet_id = "ChooseMeet",
  status_text_id = "StatusText",
  data_container_id = "DataContainer",
  sort_by_school_id = "SortBySchool",
  sort_by_gender_id = "SortByGender",
  sort_by_type_id = "SortByType",
  sort_by_time_id = "SortByTime",
  sort_by_event_id = "SortByEvent",
  sort_by_category_id = "SortByCategory",
  search_query = ""
) {
  const track_data = localStorage.getItem(TRACK_DATA);

  // get all the filter and sort elements
  const status_text = document.getElementById(status_text_id);
  const choose_meet_select = document.getElementById(choose_meet_id);
  const data_container = document.getElementById(data_container_id);
  const sort_by_school_select = document.getElementById(sort_by_school_id);
  const sort_by_gender = document.getElementById(sort_by_gender_id);
  const sort_by_type = document.getElementById(sort_by_type_id);
  const sort_by_event = document.getElementById(sort_by_event_id);
  const sort_by_time = document.getElementById(sort_by_time_id);
  const sort_by_category = document.getElementById(sort_by_category_id);

  if (!track_data) {
    status_text.textContent =
      "Cannot find track data something is wrong please try to refresh your browser or restart the application";
    status_text.style.color = "red";
    return;
  }

  // get the meet info
  const meets_info = JSON.parse(track_data);
  // get the current_meet name
  const meet_name = choose_meet_select.value;
  // get the meet that the user has selected
  const selected_meet = meets_info.find((m) => m[0].startsWith(meet_name));
  if (!selected_meet) {
    status_text.textContent =
      "Cannot find selected meet in the data. Please try to refresh your browser or reload the data.";
    status_text.style.color = "red";
    return;
  }

  // get the csv rows and header
  const csv_header = selected_meet[1][0].split(",");
  let csv_rows = selected_meet[1].slice(1).map((row) => {
    row = row.split(",");
    row[1] = row[0] + row[1];
    row.shift();
    return row;
  });

  // apply all the filers
  csv_rows = csv_rows.filter((row) => {
    // alos in this code if the field is None that means that there is no filer applied
    // school filter
    if (sort_by_school_select.value) {
      if (row[2] !== sort_by_school_select.value) return false;
    }
    // gender filter
    if (sort_by_gender.value) {
      if (row[6].toLowerCase() !== sort_by_gender.value.toLowerCase())
        return false;
    }
    // event type filter
    if (sort_by_type.value) {
      if (row[9].toLowerCase() !== sort_by_type.value.toLowerCase())
        return false;
    }
    // event filter by event name
    if (sort_by_event.value) {
      if (row[4] !== sort_by_event.value) return false;
    }
    if (sort_by_category.value) {
      if (row[1] != sort_by_category.value) return false;
    }
    if (search_query) {
      if (!row[0].toLowerCase().includes(search_query.toLowerCase()))
        return false;
    }
    return true;
  });
  update_count(csv_rows.length, "Count");
  // sort by time will be check seperately
  if (sort_by_time.value === "Earliest") {
    csv_rows.sort((a, b) => {
      return a[5] < b[5] ? -1 : a[5] > b[5] ? 1 : 0;
    });
  } else if (sort_by_time.value === "Oldest") {
    csv_rows.sort((a, b) => {
      return b[5] < a[5] ? -1 : b[5] > a[5] ? 1 : 0;
    });
  }

  // re render the table same logic in the add choose meet function
  let table = "<table style='width:100%; border-collapse: collapse;'>";
  table +=
    "<thead><tr>" +
    csv_header
      .map((h) => `<th style='border:1px solid #ccc; padding:4px;'>${h}</th>`)
      .join("") +
    "</tr></thead>";
  table += "<tbody>";
  csv_rows.forEach((row) => {
    table +=
      "<tr>" +
      row
        .map(
          (cell) =>
            `<td style='border:1px solid #ccc; padding:10px;'>${clean_string(
              cell
            )}</td>`
        )
        .join("") +
      "</tr>";
  });
  table += "</tbody></table>";
  data_container.innerHTML = table;
}

/*
this function will activates all the fitlers
*/
function setup_filters(
  choose_meet_id = "ChooseMeet",
  sort_by_school_id = "SortBySchool",
  sort_by_gender_id = "SortByGender",
  sort_by_type_id = "SortByType",
  sort_by_time_id = "SortByTime",
  sort_by_event_id = "SortByEvent",
  status_text_id = "StatusText",
  sort_by_category_id = "SortByCategory"
) {
  const status_text = document.getElementById(status_text_id);
  [
    choose_meet_id,
    sort_by_school_id,
    sort_by_gender_id,
    sort_by_type_id,
    sort_by_time_id,
    sort_by_event_id,
    sort_by_category_id,
  ].forEach((id) => {
    const element = document.getElementById(id);
    if (!element) {
      status_text.textContent = `element with id ${id} not found. Something went wrong. Please try to refresh your browser or restart the application.`;
      status_text.style.color = "red";
      return;
    }
    element.addEventListener("change", () => {
      filter_and_render_table(
        choose_meet_id,
        "StatusText",
        "DataContainer",
        sort_by_school_id,
        sort_by_gender_id,
        sort_by_type_id,
        sort_by_time_id,
        sort_by_event_id,
        sort_by_category_id
      );
    });
  });
}

function setup_search(
  search_input_id = "SearchInput",
  search_button_id = "SearchButton",
  choose_meet_id = "ChooseMeet",
  status_text_id = "StatusText",
  data_container_id = "DataContainer",
  sort_by_school_id = "SortBySchool",
  sort_by_gender_id = "SortByGender",
  sort_by_type_id = "SortByType",
  sort_by_time_id = "SortByTime",
  sort_by_event_id = "SortByEvent",
  sort_by_category_id = "SortByCategory"
) {
  const searchButton = document.getElementById(search_button_id);
  const searchInput = document.getElementById(search_input_id);

  searchButton.addEventListener("click", () => {
    filter_and_render_table(
      choose_meet_id,
      status_text_id,
      data_container_id,
      sort_by_school_id,
      sort_by_gender_id,
      sort_by_type_id,
      sort_by_time_id,
      sort_by_event_id,
      sort_by_category_id,
      searchInput.value.trim()
    );
  });
  // add even listener so the user can click enter andstills earches
  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      searchButton.click();
    }
  });
}

function main() {
  load_initial_data();
  add_load_data_button();
  add_choose_meets();
  setup_filters();
  setup_search();
}

main();

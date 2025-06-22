const TRACK_DATA = "track_meet_data";

/*
this function will take a string in then clean all alhanumeric characters of it
*/
function clean_string(str) {
  return str.replace(/[^a-zA-Z0-9\s]/g, "").trim();
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
    document.getElementById("SortBy").value = "default";
    document.getElementById("FilterGender").value = "default";
    document.getElementById("FilterType").value = "default";
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
      console.log(row);
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
  fetch("/load_initial_data", { method: "POST" })
    .then((response) => {
      if (!response.ok) throw new Error("Network response was not ok");
      return response.json();
    })
    .then((json) => {
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
    })
    .catch((error) => {
      // here display the error button
      // announce the error
      status_text.textContent = "Error: " + error.message;
      status_text.style.color = "red";
    });
}

function main() {
  load_initial_data();
  add_load_data_button();
  add_choose_meets();
}

main();

let currentId = "formFileLg1";
let currenDroptId = "drop_zone";

// function crnt(e) {
//   let allLinks = document.getElementsByClassName("dashlinks");

//   allLinks = [...allLinks];
//   allLinks.map((ini) => ini.classList.remove("active"));
//   e.target.classList.add("active");
//   currentId = e.target.id;
//   if (currentId == "gallery") {
//     currentId = "inputGroupFile01";
//     currenDroptId = "drop_zone";
//   } else if (currentId == "addnotify") {
//     currentId = "inputGroupFile02";
//     currenDroptId = "drop_zone2";
//   } else if (currentId == "update") {
//     document.getElementById("jsonData").innerHTML = "";
//     document.getElementById("jsonData2").innerHTML = "";
//     callAgain();
//     callAgain2();

//     currentId = "inputGroupFile03";
//     currenDroptId = "drop_zone3";
//   }
// }

let fileDropped = false;

function dropHandler(ev) {
  console.log("File(s) dropped");
  document.getElementById(currenDroptId).innerHTML = "";

  fileDropped = true;

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
  let list = new DataTransfer();

  if (ev.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    [...ev.dataTransfer.items].forEach((item, i) => {
      // If dropped items aren't files, reject them
      if (item.kind === "file") {
        const file = item.getAsFile();

        let filea = new File([file], file.name, {
          type: file.type,
        });
        list.items.add(filea);
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function () {
          // console.log(reader.result);
          let image = document.createElement("img");
          if (file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" || file.type == "application/pdf") {
            image.src = "doc.png";
          } else {
            image.src = reader.result;
          }
          ev.target.appendChild(image);
        };
      }
    });
    let myFileList = list.files;
    document.getElementById(currentId).files = myFileList;
    console.log(document.getElementById(currentId).files);
  } else {
    // Use DataTransfer interface to access the file(s)
    [...ev.dataTransfer.files].forEach((file, i) => {
      console.log(`… file[${i}].name = ${file.name}`);
    });
  }
  if (currentId == "formFileLg1") {
    document.getElementById("drop_zone").classList.remove("el");
  }
}
function dragOverHandler(ev) {
  console.log("File(s) in drop zone");

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
}

function clickAdd(e) {
  console.log(e.target.files);
  document.getElementById(currentId).files.length == 0 ? document.getElementById("drop_zone").classList.add("el") : document.getElementById("drop_zone").classList.remove("el");
  document.getElementById(currenDroptId).innerHTML = "";
  if (fileDropped == false) {
    [...e.target.files].map((ini) => {
      const file = ini;

      var reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = function () {
        // console.log(reader.result);
        let image = document.createElement("img");
        if (file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" || file.type == "application/pdf") {
          image.src = "doc.png";
        } else {
          image.src = reader.result;
        }
        document.getElementById(currenDroptId).appendChild(image);
      };
    });
  }
}

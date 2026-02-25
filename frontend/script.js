
const API_URL = "https://sold7hpfpqnzjvq6yr5appgxd40kddaz.lambda-url.ap-south-1.on.aws/";

// const video = document.getElementById("video");
// const result = document.getElementById("result");

// // Start camera
// navigator.mediaDevices.getUserMedia({ video: true })
// .then(stream => {
//     video.srcObject = stream;
// })
// .catch(err => {
//     result.innerText = "Camera access denied or not working";
//     console.error(err);
// });

// function capture() {

//     result.innerText = "Processing attendance...";

//     const studentId = document.getElementById("studentId").value;
//     const slot = document.querySelector('input[name="slot"]:checked')?.value;

//     if (!slot) {
//         result.innerText = "Please select a subject slot";
//         return;
// }

//     if (!studentId) {

//         result.innerText = "Please enter Student ID";
//         return;
//     }

//     const canvas = document.createElement("canvas");

//     canvas.width = video.videoWidth;
//     canvas.height = video.videoHeight;

//     const ctx = canvas.getContext("2d");

//     ctx.drawImage(video, 0, 0);

//     const imageBase64 = canvas.toDataURL("image/jpeg").split(",")[1];

//     fetch(API_URL, {

//         method: "POST",

//         headers: {
//             "Content-Type": "application/json"
//         },

//         body: JSON.stringify({

//             student_id: studentId,
//             slot_id: slot,
//             image: imageBase64

//         })

//     })
//     .then(response => response.json())

//     .then(data => {

//         result.innerText = data.message;

//     })

//     .catch(error => {

//         result.innerText = "Error submitting attendance";
//         console.error(error);

//     });

// // }
// const API_URL="YOUR_LAMBDA_FUNCTION_URL";


const video=document.getElementById("video");

const result=document.getElementById("result");



navigator.mediaDevices.getUserMedia({video:true})

.then(stream=>{

video.srcObject=stream;

});



const today=new Date();


document.getElementById("date").innerText =
today.toLocaleDateString('en-US', {

month: 'short',
day: 'numeric',
year: 'numeric'

});


document.getElementById("day").innerText=

today.toLocaleString('en-US',{weekday:'long'});



function capture(){



const studentId=document.getElementById("studentId").value;


const slot=document.querySelector('input[name="slot"]:checked')?.value;



if(!studentId||!slot){

result.innerText="Enter student ID and select slot";

return;

}



const canvas=document.createElement("canvas");


canvas.width=video.videoWidth;


canvas.height=video.videoHeight;


const ctx=canvas.getContext("2d");


ctx.drawImage(video,0,0);



video.classList.add("face-detected");



setTimeout(()=>{

video.classList.remove("face-detected");

},2000);



const image=canvas.toDataURL("image/jpeg").split(",")[1];



fetch(API_URL,{


method:"POST",


headers:{

"Content-Type":"application/json"

},


body:JSON.stringify({


student_id:studentId,


slot_id:slot,


image:image


})


})


.then(res=>res.json())


.then(data=>{


result.innerText=data.message;



if(data.message.includes("successful")){


showPopup();


}


})

.catch(()=>{


result.innerText="Error marking attendance";


});


}



function showPopup(){

document.getElementById("popup").style.display="flex";

}



function closePopup(){

document.getElementById("popup").style.display="none";

}
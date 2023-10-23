import React, {useState} from 'react';
import {FileUploader} from "react-drag-drop-files";
import axios from "axios";

function HomePage() {
    const [file, setFile] = useState(null);
    const handleChange = (file) => {
        setFile(file);
        console.log(file);
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            // Send POST request to backend API using Axios
            axios.post('http://127.0.0.1:8000/api/files/', formData)
                .then(response => {
                    // Handle a successful response from the server
                    console.log('File uploaded successfully');
                })
                .catch(error => {
                    // Handle errors here
                    console.error('File upload failed', error);
                });
        }

    };
    return (
        <FileUploader handleChange={handleChange} name="file"/>
    );
}

export default HomePage;

import React, {useState} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
import Modal from 'react-modal';

const customStyles = {
    content: {
        top: '50%',
        left: '50%',
        right: 'auto',
        bottom: 'auto',
        marginRight: '-50%',
        transform: 'translate(-50%, -50%)',
    },
};

function DownloadFile() {
    const [passcode, setPasscode] = useState('');
    const [fileData, setFileData] = useState(null);
    const [errorMsg, setErrorcode] = useState('');
    let subtitle;
    const [modalIsOpen, setIsOpen] = React.useState(false);
    const apiHost = process.env.REACT_APP_API_HOST || 'localhost';
    const apiPort = process.env.REACT_APP_API_PORT || '8000';

    const apiUrl = `${apiHost}:${apiPort}`;

    function openModal() {
        setIsOpen(true);
    }

    function afterOpenModal() {
        // references are now sync'd and can be accessed.
        subtitle.style.color = '#f00';
    }

    function closeModal() {
        setIsOpen(false);
    }

    const handlePasscodeChange = (e) => {
        setPasscode(e.target.value);
    };

    const handleDownloadFile = () => {
        if (passcode) {
            axios.get(`http://${apiUrl}/api/files/${passcode}/`, {responseType: 'blob'})
                .then(response => {
                    let filename = 'downloaded_file'; // Default filename
                    let mimeType = 'application/octet-stream'; // Default MIME type

                    // Check if the Content-Disposition header exists
                    if (response.headers['content-disposition']) {
                        const contentDisposition = response.headers['content-disposition'];
                        const filenameMatch = contentDisposition.match(/filename="(.+)"/);

                        if (filenameMatch) {
                            filename = filenameMatch[1];
                        }

                        // Check if the Content-Type header exists
                        if (response.headers['content-type']) {
                            mimeType = response.headers['content-type'];
                            console.log(mimeType);
                        }
                    }

                    const blob = new Blob([response.data], {type: mimeType});

                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = filename;

                    a.style.display = 'none';
                    document.body.appendChild(a);
                    a.click();

                    // Clean up the temporary URL and remove the dynamically created anchor element
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                })
                .catch(error => {
                    console.log(error);
                    openModal();
                    // Change the error message once error message is added to the response
                    setErrorcode("File not found");
                });
        }
    };


    return (
        <div className="h-screen flex flex-col items-center justify-center bg-gray-100">
            <div>
                <Modal
                    isOpen={modalIsOpen}
                    onAfterOpen={afterOpenModal}
                    onRequestClose={closeModal}
                    style={customStyles}
                    contentLabel="Error Modal"
                    ariaHideApp={false}
                >
                    <h2 ref={(_subtitle) => (subtitle = _subtitle)}>Error</h2>
                    <div className="sm (640px) py-2">
                        {errorMsg}
                    </div>
                    <button className="bg-red-500 hover:bg-blue-600 text-white py-2 px-4 mx-2 rounded-lg w-48"
                            onClick={closeModal}>close
                    </button>
                </Modal>
            </div>
            <div className="border p-6 rounded-lg bg-white shadow-md w-96 relative">
                <Link to="/" className="absolute top-2 right-2 text-gray-600 text-sm hover:text-blue-600">
                    Back
                </Link>
                <h1 className="text-2xl font-bold mb-4">Download File</h1>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Enter Passcode:
                    </label>
                    <input
                        type="text"
                        value={passcode}
                        onChange={handlePasscodeChange}
                        className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300"
                    />
                </div>
                <button onClick={handleDownloadFile}
                        className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full">
                    Download File
                </button>
            </div>
        </div>
    );
}

export default DownloadFile;

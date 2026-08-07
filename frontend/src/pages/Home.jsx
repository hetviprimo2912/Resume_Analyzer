import { useState } from "react";

import UploadScreen from "../components/UploadScreen";
import ChatLayout from "../components/ChatLayout";

import "../styles/home.css";

function Home() {

    const [resumeId, setResumeId] = useState("");

    return (

        <div className="home">

            {
                resumeId
                    ? (
                        <ChatLayout
                            resumeId={resumeId}
                        />
                    )
                    : (
                        <UploadScreen
                            onUploadSuccess={setResumeId}
                        />
                    )
            }

        </div>

    );

}

export default Home;
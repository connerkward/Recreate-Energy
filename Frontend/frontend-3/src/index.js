import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import "./Constants/constants.css"
import { Amplify, } from 'aws-amplify'
import '@aws-amplify/ui-react/styles.css';
import {
    Authenticator,
    useTheme,
    View,
    Image,
    Text,
} from '@aws-amplify/ui-react';
import awsconfig from './aws-exports.js'

Amplify.configure(awsconfig)
document.title = "Recreate Dashboard";  

const components = {
    Header() {
        const { tokens } = useTheme();

        return (
            <View textAlign="center" padding={tokens.space.small}>
                <Image
                    alt="Recreate logo"
                    src="https://static.wixstatic.com/media/c21af6_1acfa0544d444d7c85420aa3e068c266~mv2.png/v1/fill/w_644,h_270,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/white_logo_transparent_background.png"
                />
            </View>
        );
    },
    Footer() {
        const { tokens } = useTheme();
        return (
            <View textAlign="center" padding={tokens.space.large}>
                <Text color={`${tokens.colors.white}`}>
                    &copy; All Rights Reserved
                </Text>
            </View>
        );
    },

}
const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
    <div className="outer">
        <Authenticator
            // socialProviders={['amazon', 'apple', 'facebook', 'google']} 
            components={components}
            hideSignUp={true}
        ><App />
        </Authenticator>
        <footer style={{ width: "100%", position: "fixed", bottom: 0, fontSize: "small", paddingLeft: "var(--margin-sides)", height: "var(--footer-height)", backgroundColor: "var(--bg-color)" }}>
            <code>Recreate Energy Internal Only -- API 0.6</code>
        </footer>
    </div>)

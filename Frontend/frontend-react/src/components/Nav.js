
import { Link } from "react-router-dom";

const Nav = (props) => {
    return <nav style={{display: "flex", flexDirection:"row", gap: "1rem", marginBottom:"1rem"}}>
        {Object.entries(props.PAGES).map(([pageKey, pageValues], i) => {
            const navLink = <div key={`NavLink${i}-${pageKey}`}>
                <Link to={pageValues.url} element={<pageValues.component />}>{pageValues.component.displayName}</Link>
            </div>
            if (props.NAVPAGESKEYS.includes(pageKey)) return navLink
        })}

    </nav>;
};

Nav.displayName = "Nav"

export default Nav;
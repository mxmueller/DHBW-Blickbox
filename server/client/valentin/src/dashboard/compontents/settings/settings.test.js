import React from "react";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import Settings from "./Settings";

jest.mock("./settings.alerts.js", () => () => <div>Mock AlertSettings</div>);

describe("Settings Component", () => {
  test("renders without crashing", () => {
    render(<Settings />);
    expect(screen.getByTestId("settings-icon")).toBeInTheDocument();
  });
});

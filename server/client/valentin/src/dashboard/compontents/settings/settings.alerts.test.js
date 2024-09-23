import React from "react";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import UserSettings from "./settings.alerts";

jest.mock("js-cookie", () => ({
  get: jest.fn(),
  set: jest.fn(),
}));

Object.defineProperty(window, "Notification", {
  value: jest.fn(),
});

describe("UserSettings Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders checkbox for push notifications", () => {
    render(<UserSettings />);
    const checkbox = screen.getByRole("checkbox", {
      name: /Push-Benachrichtigung erhalten/i,
    });
    expect(checkbox).toBeInTheDocument();
    expect(checkbox).not.toBeChecked();
  });
});

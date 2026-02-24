package pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

import factory.DriverFactory;

public class LoginPage {

	private WebDriver driver;// WebDriver driver = DriverFactory.getDriver();

	public LoginPage() {
		this.driver = DriverFactory.getDriver();
	}

	private By email = By.xpath("//input[@name='email'][contains(@data-qa,'login-email')]");
	private By password = By.xpath("//input[@name='password']");
	private By loginBtn = By.xpath("//button[normalize-space()='Login']");
	private By loggedInText = By.xpath("//a[contains(text(),'Logged in as')]");

	public String getLoggedInUsername() {
		return driver.findElement(loggedInText).getText();

	}

	public void login(String user, String pass) {
		driver.findElement(email).sendKeys(user);
		driver.findElement(password).sendKeys(pass);
		driver.findElement(loginBtn).click();
	}
}

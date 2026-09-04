package pages;

import java.time.Duration;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import factory.DriverFactory;
import util.WaitUtil;
public class AddToCart {

	private WebDriver driver;

	public AddToCart() {
		this.driver = DriverFactory.getDriver();
	}

	private By MenDD = By.xpath("//a[normalize-space()='Men']");
	private By Category = By.xpath("//a[normalize-space()='Tshirts']");
	private By Brand = By.xpath("//a[@href='/brand_products/Allen Solly Junior']");
	private By ProductName = By
			.xpath("//div[@class='productinfo text-center']//p[contains(text(),'Colour Blocked Shirt – Sky Blue')]");
	private By ViewProduct = By.xpath("(//a[contains(text(),'View Product')])[3]");
	private By AddToCart = By.xpath("//button[normalize-space()='Add to cart']");
	//private By Popup = By.xpath("//p[normalize-space()='Your product has been added to cart.']");

	public void AddToCartProduct() {
		driver.get("https://automationexercise.com/brand_products/Allen%20Solly%20Junior");
		driver.findElement(MenDD).click();
		driver.findElement(Category).click();
		
		WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

		WebElement brandElement = wait.until(
		    ExpectedConditions.elementToBeClickable(Brand)
		);

		brandElement.click();
		driver.findElement(Brand).click();
		driver.findElement(ProductName).click();
		driver.findElement(ViewProduct).click();
		driver.findElement(AddToCart).click();
		//driver.findElement(Popup).click();

	}
}

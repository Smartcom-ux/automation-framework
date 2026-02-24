package pages;
import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.*;
import factory.DriverFactory;
import java.time.Duration;

public class BasePage {
	 protected WebDriver driver;
	    protected WebDriverWait wait;
public BasePage() {
	driver = DriverFactory.getDriver();
    wait = new WebDriverWait(driver, Duration.ofSeconds(10));
}

protected void click(By locator) {
    wait.until(ExpectedConditions.elementToBeClickable(locator)).click();
}

protected void type(By locator, String text) {
    wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).sendKeys(text);
}

protected String getText(By locator) {
    return wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).getText();
}
}
	
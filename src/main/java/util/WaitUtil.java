package util;
import factory.DriverFactory;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;

import java.time.Duration;
public class WaitUtil {
	public static void waitForVisibility(By locator) {

        WebDriverWait wait = new WebDriverWait(
                DriverFactory.getDriver(),
                Duration.ofSeconds(10));

        wait.until(ExpectedConditions
                .visibilityOfElementLocated(locator));
    }
}



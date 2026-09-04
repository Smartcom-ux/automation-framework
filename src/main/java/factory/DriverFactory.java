package factory;

import java.time.Duration;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;

import io.github.bonigarcia.wdm.WebDriverManager;

public class DriverFactory {

	 private static ThreadLocal<WebDriver> driver = new ThreadLocal<>();

	    public static void initDriver() {

	        String browser = System.getProperty("browser", "chrome");

	        switch (browser.toLowerCase()) {

	            case "chrome":
	                WebDriverManager.chromedriver().setup();
	                ChromeOptions chromeOptions = new ChromeOptions();
	                chromeOptions.addArguments("--disable-notifications");
	                chromeOptions.addArguments("--disable-infobars");
	                chromeOptions.addArguments("--disable-popup-blocking");
	                chromeOptions.addArguments("--disable-extensions");
	                chromeOptions.addArguments("--disable-blink-features=AutomationControlled");
	                chromeOptions.addArguments("--disable-features=IsolateOrigins,site-per-process");
	                chromeOptions.addArguments("--disable-features=InterestFeedContentSuggestions");
	                chromeOptions.addArguments("--disable-site-isolation-trials");
	                chromeOptions.addArguments("--disable-dev-shm-usage");
	                chromeOptions.addArguments("--no-sandbox");
	                addHeadlessIfRequired(chromeOptions);
	                driver.set(new ChromeDriver(chromeOptions));
	                break;

	            case "firefox":
	                WebDriverManager.firefoxdriver().setup();
	                FirefoxOptions firefoxOptions = new FirefoxOptions();
	                addHeadlessIfRequired(firefoxOptions);
	                driver.set(new FirefoxDriver(firefoxOptions));
	                break;

	            case "edge":
	                WebDriverManager.edgedriver().setup();
	                driver.set(new EdgeDriver());
	                break;

	            default:
	                throw new RuntimeException("Browser not supported: " + browser);
	        }

	        driver.get().manage().window().maximize();
	        //driver.get().manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
	        driver.get().manage().timeouts().implicitlyWait(Duration.ofSeconds(2));
	    }

	    private static void addHeadlessIfRequired(ChromeOptions options) {
	        if (Boolean.parseBoolean(System.getProperty("headless", "false"))) {
	            options.addArguments("--headless=new");
	            options.addArguments("--no-sandbox");
	            options.addArguments("--disable-dev-shm-usage");
	        }
	    }

	    private static void addHeadlessIfRequired(FirefoxOptions options) {
	        if (Boolean.parseBoolean(System.getProperty("headless", "false"))) {
	            options.addArguments("--headless");
	        }
	    }

	    public static WebDriver getDriver() {
	        return driver.get();
	    }

	    public static void quitDriver() {
	        driver.get().quit();
	        driver.remove();
	    }
	}
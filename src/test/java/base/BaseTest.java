package base;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

import factory.DriverFactory;
import util.ConfigReader;
public class BaseTest {
	 @BeforeMethod(alwaysRun = true)
	    public void setUp() {

	        // Initialize browser (based on system property)
	        DriverFactory.initDriver();

	        // Navigate to application URL
	        DriverFactory.getDriver()
	                     .get(ConfigReader.get("url"));
	    }

	    @AfterMethod(alwaysRun = true)
	    public void tearDown() {

	        // Quit browser safely
	        DriverFactory.quitDriver();
	    }
	}

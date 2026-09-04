package util;
import factory.DriverFactory;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.UUID;


public class ScreenshotUtil {
	 public static void capture(String testName) {
		 String randomString = UUID.randomUUID().toString();
	        File src = ((TakesScreenshot)
	                DriverFactory.getDriver())
	                .getScreenshotAs(OutputType.FILE);

	        File dest = new File("screenshots/"
	                + testName +randomString+ ".png");

	        dest.getParentFile().mkdirs();

	        try {
	            Files.copy(src.toPath(), dest.toPath());
	        } catch (IOException e) {
	            e.printStackTrace();
	        }
	    }
	}


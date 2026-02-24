package test;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.testng.Assert;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;

import base.BaseTest;
import listeners.TestListener;
import pages.AddToCart;
import pages.LoginPage;
import factory.DriverFactory;

@Listeners(listeners.TestListener.class)
public class TestCaserunner extends BaseTest {
	private static final Logger logger = LogManager.getLogger(TestCaserunner.class);

	@Test(retryAnalyzer = listeners.RetryAnalyzer.class, priority = 1)
	public void loginTest() {
		logger.info("Starting login test");
		LoginPage loginPage = new LoginPage();
		loginPage.login("testuser447@yopmail.com", "Pass@1234");

		String actualText = loginPage.getLoggedInUsername();
		Assert.assertTrue(actualText.contains("user2"), "Incorrect username displayed after login");
		logger.info(" login test finish");
	}

	@Test(retryAnalyzer = listeners.RetryAnalyzer.class, priority = 2)
	public void AddToProduct() {
		logger.info("AddToProduct Start");
		AddToCart addTocart = new AddToCart();
		addTocart.AddToCartProduct();
		logger.info("Finish Add To Cart");
	}
}

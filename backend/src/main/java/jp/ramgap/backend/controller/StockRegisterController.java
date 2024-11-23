package jp.ramgap.backend.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import jp.ramgap.backend.model.StockRegisteredByUser;

@RestController
@RequestMapping("/api/stock-register")
@CrossOrigin(origins = "http://localhost:3000") // React側のURLを許可
public class StockRegisterController {
    private final List<StockRegisteredByUser> stocks = new ArrayList<>();

    @PostMapping
    public String postStock(@RequestBody StockRegisteredByUser stockRegisteredByUser) {
        stocks.add(stockRegisteredByUser);

        return "Stock Registered successfully!";
    }

    @GetMapping
    public List<StockRegisteredByUser> getStocks() {
        return stocks;
    }

}

package jp.ramgap.backend.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import jp.ramgap.backend.form.StocksAddForm;

@RestController
@RequestMapping("/api/stocks")
@CrossOrigin(origins = "http://localhost:3000") // React側のURLを許可
public class StocksController {
    private final List<StocksAddForm> stocks = new ArrayList<>();

    @PostMapping
    public String postStocks(@RequestBody StocksAddForm stockRegisteredByUser) {
        stocks.add(stockRegisteredByUser);

        return "Stock Registered successfully!";
    }

    @GetMapping
    public List<StocksAddForm> getStocks() {
        return stocks;
    }

}

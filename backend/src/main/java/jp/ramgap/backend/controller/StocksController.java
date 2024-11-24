package jp.ramgap.backend.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.ObjectError;
import org.springframework.validation.annotation.Validated;
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
    public ResponseEntity<?> postStocks(@Validated @RequestBody StocksAddForm stocksAddForm, BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            StringBuilder errorMessage = new StringBuilder();
            for (ObjectError error : bindingResult.getAllErrors()) {
                errorMessage.append(error.getDefaultMessage()).append("; ");
            }
            return ResponseEntity.badRequest().body(errorMessage.toString());
        }
        
        stocks.add(stocksAddForm);

        return ResponseEntity.ok("Stock info added successfully!");
    }

    @GetMapping
    public List<StocksAddForm> getStocks() {
        return stocks;
    }

}
